import requests
import tqdm
import json
import sys
import os
import shutil
import subprocess
import time
import m3u8
import urllib.parse
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from . import utils


class ProcessM3U8:

    def __init__(self, args):
        self.args = args
        self.merged_file_size = 0
        self.has_seperate_audio = False
        self.has_subtitle = False
        # updating merge ts file path
        if args.output.endswith(".srt"):
            self.merged_tsfile_path = args.output.replace(".srt", ".vtt")
        else:
            self.merged_tsfile_path = os.path.splitext(args.output)[0] + ".ts"
        # check for ffmpeg installation
        if not args.output.endswith(".ts"):
            self._check_ffmpeg_path()
        # downloading clients and sessions
        self.http_client = m3u8.DefaultHTTPClient()
        self.download_session = requests.Session()
        # updating headers
        self.headers = {}
        if args.headers is not None:
            with open(self.args.headers) as f:
                self.headers = json.load(f)
            
            self.download_session.headers.update(self.headers)
            print(f"headers are updated to: {self.download_session.headers}")
        # updating proxies
        proxies = {}
        if args.proxy_address is not None:
            proxies["https" if args.proxy_address.startswith("https") else "http"] = args.proxy_address
            self.http_client = m3u8.DefaultHTTPClient(proxies)
            self.download_session.proxies.update(proxies)
            print(f"proxies are updated to: {self.download_session.proxies}")

    @staticmethod
    def runtime_error(msg="no message specified", code=1):
        print(f"error: {msg}")
        sys.exit(code)

    @staticmethod
    def find_absolute_uri(baseurl, m3u8_data):
        if baseurl is None:
            return m3u8_data.absolute_uri
        else:
            return urllib.parse.urljoin(baseurl, m3u8_data.uri) if not m3u8_data.uri.startswith("http") else m3u8_data.uri
    
    @staticmethod
    def decrypt_aes_data(cipher_data, key, iv):
        cipher_data = pad(data_to_pad=cipher_data, block_size=AES.block_size)
        return AES.new(key=key, mode=AES.MODE_CBC, IV=iv).decrypt(cipher_data)

    def _find_key(self, baseurl, segment):
        if self.args.key_iv is not None:
            return f"b'{self.args.key_iv.split('==>')[0]}'"

        if segment.key is not None:
            key_absolute_uri = self.find_absolute_uri(baseurl, segment.key)
            key = b""
            for chunk in self.download_session.get(key_absolute_uri):
                key += chunk
            return f"{key}"
        else:
            return None

    def _find_iv(self, baseurl, segment):
        if self.args.key_iv is not None:
            return f"{self.args.key_iv.split('==>')[1]}"

        if segment.key is not None:
            return segment.key.iv.replace("0x", "")
        else:
            return None

    def _check_ffmpeg_path(self):
        if self.args.ffmpeg_path == "ffmpeg" and shutil.which(self.args.ffmpeg_path) is None:
            self.runtime_error("ffmpeg is not installed, visit https://ffmpeg.org/download.html")
        elif self.args.ffmpeg_path != "ffmpeg" and not os.path.isfile(self.args.ffmpeg_path):
            self.runtime_error("ffmpeg is not installed, visit https://ffmpeg.org/download.html")

    def parse_link_file(self):
        return self.args.input, self.args.baseurl

    def parse_log_json(self):
        with open(self.args.input) as f:
            json_data = json.load(f)

        if self.args.pre_select is None:
            print(f"m3u8 urls listed inside {self.args.input}:")
            for i, m3u8_url in enumerate(json_data["m3u8_urls"]):
                print(f"{i+1}) {m3u8_url}")
            
            print()
            target_url = int(input("choose a m3u8 url (1, 2, etc.): "))
            print()
            target_url = json_data["m3u8_urls"][target_url - 1]
        
        else:
            target_url = json_data["m3u8_urls"][self.args.pre_select]
        
        if self.args.baseurl is None:
            baseurl = json_data["baseurl"]
        else:
            baseurl = self.args.baseurl
        
        return target_url, baseurl

    def _segments_from_variant_playlists(self, m3u8_file, baseurl):
        print("m3u8 playlists listed inside m3u8 file:")

        for i, m3u8_playlists in enumerate(m3u8_file.data["playlists"]):
            print(f"-------------------- {i + 1} --------------------")
            for spec, val in m3u8_playlists["stream_info"].items():
                print(f"{spec}: {val}")

        print()
        selected_playlist = int(input("choose a m3u8 playlist (1, 2, etc.): "))
        print()
        m3u8_playlist_file = m3u8_file.playlists[selected_playlist - 1]
        playlist_absolute_uri = self.find_absolute_uri(baseurl, m3u8_playlist_file)
        print(f"fetching segments from m3u8 playlist: {playlist_absolute_uri}")
        return m3u8.load(playlist_absolute_uri, headers=self.headers, http_client=self.http_client).segments

    def _segments_of_media_playlists(self, m3u8_file, baseurl):
        for media_stream in m3u8_file.media:
            args_dict = {}
            for key, value in self.args._get_kwargs():
                args_dict[key] = value

            if media_stream.autoselect == "YES" and media_stream.type == "AUDIO":
                print("info: retargeting to download seperate audio stream")
                self.has_seperate_audio = True
                self._check_ffmpeg_path()
                args_dict["input"] = self.find_absolute_uri(baseurl, media_stream)
                args_dict["output"] = "merged_audio.ts"
                args_dict["tempdir"] = args_dict["tempdir"] + "_audio"
                command_save(Namespace(**args_dict))

            elif media_stream.autoselect == "YES" and media_stream.type == "SUBTITLES":
                print("info: retargeting to download subtitle stream")
                self.has_subtitle = True
                args_dict["input"] = self.find_absolute_uri(baseurl, media_stream)
                args_dict["output"] = "merged_subtitle.srt"
                args_dict["tempdir"] = args_dict["tempdir"] + "_subtitle"
                command_save(Namespace(**args_dict))

    def parse_m3u8(self, parsed_links):
        target_url, baseurl = parsed_links
        print(f"fetching m3u8 content: {target_url}")

        try:
            m3u8_file = m3u8.load(target_url, headers=self.headers, http_client=self.http_client)
            segments = m3u8_file.segments

            if m3u8_file.is_variant:
                segments = self._segments_from_variant_playlists(m3u8_file, baseurl)

            if m3u8_file.media != []:
                self._segments_of_media_playlists(m3u8_file, baseurl)

            return segments

        except Exception as e:
            print(e.__str__())
            self.runtime_error("failed to fetch m3u8 content")

    # this function uses binary merge method for merging ts files
    def _ts_merge_task(self, total_ts_files):
        print()
        print("ts file merge task")
        print(f"starting in {self.args.timeout} seconds...")
        time.sleep(self.args.timeout)
        print()

        filename = self.merged_tsfile_path if not self.has_seperate_audio else "merged_video.ts"
        with open(filename, "wb") as f:
            for i in tqdm.trange(1, total_ts_files + 1):
                try:
                    with open(f"{self.args.tempdir}/{i}.ts", "rb") as f2:
                        f.write(f2.read())
                except FileNotFoundError:
                    self.runtime_error(f"{i}.ts file is missing")
                
    def _ffmpeg_covert_task(self):
        print()
        print("running ffmpeg convert task")
        print(f"starting in {self.args.timeout} seconds...")

        ffmpeg_command = [
            self.args.ffmpeg_path, "-i",
            self.merged_tsfile_path if not self.has_seperate_audio else "merged_video.ts"
        ]
        
        if self.has_seperate_audio:
            ffmpeg_command.extend(["-i", "merged_audio.ts"])

        if self.has_subtitle:
            ffmpeg_command.extend(["-i", "merged_subtitle.srt"])

        if not self.merged_tsfile_path.endswith(".vtt"):
            ffmpeg_command.extend(["-c", "copy"])
            
        ffmpeg_command.append(self.args.output)
        print(f"executing command: {' '.join(ffmpeg_command)}")

        try:
            subprocess.run(ffmpeg_command)
        except Exception as e:
            print(e.__str__())
            print(f"info: temporary merged ts file is saved at {self.merged_tsfile_path}")
            self.runtime_error("ts conversion failed")

    def _clean_up_task(self):
        print()
        print("clean up task")
        print(f"starting in {self.args.timeout} seconds...")
        time.sleep(self.args.timeout)

        try:
            shutil.rmtree(self.args.tempdir)
            
            if not self.args.output.endswith(".ts") and not self.has_seperate_audio:
                os.remove(self.merged_tsfile_path)
                
            if self.has_seperate_audio:
                os.remove("merged_audio.ts")
                os.remove("merged_video.ts")
            
            if self.has_subtitle:
                os.remove("merged_subtitle.srt")

        except Exception as e:
            print(e.__str__())
            self.runtime_error("clean up task failed")

    def _download_segment_in_thread(self, segment_dict):
        filename = f"{self.args.tempdir}/{segment_dict['index']}.ts"
        info_filename =f"{self.args.tempdir}/{segment_dict['index']}_info.json"
        
        # dumping segment info to a json file
        with open(info_filename, "w", encoding="utf-8") as f:
            json.dump(segment_dict, f, indent=4)

        try:
            response = self.download_session.get(segment_dict["uri"], stream=True)	
            ts_file_size = int(response.headers.get("Content-Length", 0))
            # skip re-downloading of ts file if it exists with original size
            download_ts = False
            if os.path.isfile(filename):
                if round(os.stat(filename).st_size) != round(ts_file_size):
                    download_ts = True
            else:
                download_ts = True

            start = time.perf_counter()
            if download_ts:
                with open(filename, "wb") as f:
                    encrypted_ts_data = b""
                    
                    for data in response.iter_content(self.args.chunk_size):
                        if segment_dict["key"] is not None:
                            encrypted_ts_data += data
                        else:
                            f.write(data)
                    
                    if segment_dict["key"] is not None:
                        try:
                            f.write(self.decrypt_aes_data(encrypted_ts_data, eval(segment_dict["key"]), segment_dict["iv"]))
                        except Exception as e:
                            print(f"\nerror: segment {segment_dict['index']} decryption failed\n")
                            print(e.__str__())
                            os._exit(1)

        except Exception as e:
            # update retrycount on each failed call
            if segment_dict["retrycount"] <= self.args.retry_count:
                segment_dict["retrycount"] += 1

                with open(info_filename, "w", encoding="utf-8") as f:
                    json.dump(segment_dict, f, indent=4)

                print(f"info: segment {segment_dict['index']} added to retry queue {segment_dict['retrycount']}")
                return 1 # this return ensures that progress bar is not updated 
            else:
                print("\nerror: download failed, re-run the command with --no-cleanup flag to resume download\n")
                print(e.__str__())
                os._exit(1)

        # download status sync
        self.process_segments.update(1)
        self.merged_file_size += ts_file_size
        estimated_size = (self.merged_file_size / self.process_segments.n) * (self.total_ts_files)
        download_speed = ts_file_size / (time.perf_counter() - start)
        self.process_segments.set_description(f"{utils.convertbytes(self.merged_file_size)[0]}/{utils.convertbytes(estimated_size)[0]}, " + 
                                         f"{utils.convertbytes(download_speed)[0].replace(' ', '')}/s")

    def download_in_mutiple_thread(self, segments, parsed_links):
        if os.path.exists(self.args.tempdir) and self.args.cleanup:
            shutil.rmtree(self.args.tempdir)
            os.mkdir(self.args.tempdir)
        elif not os.path.exists(self.args.tempdir):
            os.mkdir(self.args.tempdir)
            
        self.total_ts_files = len(segments)
        processed_ts_index = 1
        
        with tqdm.tqdm(total=self.total_ts_files, desc="0 KB/0 KB, 0KB/s", unit="segment") as self.process_segments:
            with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
                for segment in segments:
                    segment_dict = {
                        "uri": self.find_absolute_uri(parsed_links[1], segment),
                        "key": self._find_key(parsed_links[1], segment),
                        "iv": self._find_iv(parsed_links[1], segment),
                        "index": processed_ts_index,
                        "retrycount": 0
                    }

                    processed_ts_index += 1
                    executor.submit(self._download_segment_in_thread, segment_dict)

            # retry pool
            while self.process_segments.n != self.total_ts_files:
                with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
                    for i in range(1, self.total_ts_files + 1):
                        with open(f"{self.args.tempdir}/{i}_info.json") as f:
                            segment_dict = json.load(f)
                        
                        if segment_dict["retrycount"] != 0 and segment_dict["retrycount"] <= self.args.retry_count:
                            executor.submit(self._download_segment_in_thread, segment_dict)
                        elif segment_dict["retrycount"] >= self.args.retry_count:
                            break
        
        # post tasks
        self._ts_merge_task(self.total_ts_files)
        if not self.args.output.endswith(".ts") or self.has_seperate_audio or self.has_subtitle:
            self._ffmpeg_covert_task()
        if self.args.cleanup:
            self._clean_up_task()	

def command_save(args):
    m3u8_downloader = ProcessM3U8(args)
    
    if args.input.endswith(".json"):
        parsed_links = m3u8_downloader.parse_log_json()	
    else:
        parsed_links = m3u8_downloader.parse_link_file()

    segments = m3u8_downloader.parse_m3u8(parsed_links)
    print(f"file will be saved at: {args.output}")
    print(f"starting download in {args.threads} thread/s\n")
    m3u8_downloader.download_in_mutiple_thread(segments, parsed_links)	
    print(f"\nfile downloaded successfully at: {args.output}")

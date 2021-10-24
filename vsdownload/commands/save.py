import requests
import tqdm
import json
import sys
import os
import shutil
import subprocess
import time
import m3u8
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from typing import NoReturn, Tuple, Optional, Union
from rich.console import Console
from . import utils


console = Console()


class ProcessM3U8:
    """class for processing m3u8 data from segments parsing to downloading it"""

    def __init__(self, args: Namespace, check: Optional[bool] = False) -> None:
        """constructor for ProcessM2U8 class

        Args:
            args (Namespace): supplied arguments in argsparse.Namespace object
            check (Optional[bool], optional): raises RuntimeError instead of sys.exit(1). Defaults to False.
        """
        self.args = args
        self.check = check
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
            console.print(f"headers are updated to: {self.download_session.headers}")
        # updating proxies
        if args.proxy_address is not None:
            proxies = {
                "https" if args.proxy_address.startswith("https") else "http": args.proxy_address
            }

            self.http_client = m3u8.DefaultHTTPClient(proxies)
            self.download_session.proxies.update(proxies)
            console.print(f"proxies are updated to: {self.download_session.proxies}")

    def parse_link_file(self) -> Tuple[str, str]:
        """parse out target m3u8 uri or file + baseurl

        Returns:
            Tuple[str, str]: tuple with format (target m3u8 uri or file, baseurl)
        """
        return self.args.input, self.args.baseurl

    def parse_log_json(self) -> Tuple[str, str]:
        """parse out target m3u8 uri + baseurl from log.json file

        Returns:
            Tuple[str, str]: tuple with format (target m3u8 uri, baseurl)
        """
        with open(self.args.input) as f:
            json_data = json.load(f)

        if self.args.pre_select is None:
            print(f"m3u8 urls listed inside {self.args.input}:")
            for i, m3u8_url in enumerate(json_data["m3u8_urls"]):
                print(f"{i+1}) {m3u8_url}")
            
            target_url = int(input("\nchoose a m3u8 url (1, 2, etc.): "))
            print()
            target_url = json_data["m3u8_urls"][target_url - 1]
        
        else:
            target_url = json_data["m3u8_urls"][self.args.pre_select]
        
        if self.args.baseurl is None:
            baseurl = json_data["baseurl"]
        else:
            baseurl = self.args.baseurl
        
        return target_url, baseurl

    def parse_m3u8(self, parsed_links: Tuple[str, str]) -> m3u8.SegmentList:
        """parse m3u8 segments from parsed links

        Args:
            parsed_links (Tuple[str, str]): [description]

        Returns:
            m3u8.SegmentList: segments object
        
        Note:
            for seperate audio and subtitle stream this method internally call another instance of base class and downloads it
        """
        target_url, baseurl = parsed_links
        console.print(f"fetching m3u8 content: {target_url}")

        try:
            m3u8_file = m3u8.load(target_url, headers=self.headers, http_client=self.http_client)
            segments = m3u8_file.segments

            if m3u8_file.is_variant:
                segments = self._segments_from_variant_playlists(m3u8_file, baseurl)

            if m3u8_file.media != []:
                self._segments_of_media_playlists(m3u8_file, baseurl)

            return segments

        except Exception as e:
            self.print_exception(e)
            self._runtime_error("failed to fetch m3u8 content")
            
    def _segments_from_variant_playlists(self, m3u8_file: m3u8.M3U8, baseurl: Union[str, None]) -> None:
        print("m3u8 playlists listed inside m3u8 file:")

        for i, m3u8_playlists in enumerate(m3u8_file.data["playlists"]):
            print(f"-------------------- {i + 1} --------------------")
            for spec, val in m3u8_playlists["stream_info"].items():
                print(f"{spec}: {val}")

        selected_playlist = int(input("\nchoose a m3u8 playlist (1, 2, etc.): "))
        m3u8_playlist_file = m3u8_file.playlists[selected_playlist - 1]
        playlist_absolute_uri = utils.find_absolute_uri(baseurl, m3u8_playlist_file)
        console.print(f"\nfetching segments from m3u8 playlist: {playlist_absolute_uri}")
        return m3u8.load(playlist_absolute_uri, headers=self.headers, http_client=self.http_client).segments

    def _segments_of_media_playlists(self, m3u8_file: m3u8.M3U8, baseurl: Union[str, None]) -> None:
        for media_stream in m3u8_file.media:
            args_dict = {key: value for key, value in self.args._get_kwargs()}

            if media_stream.type == "AUDIO" and media_stream.autoselect == "YES":
                self.print_info("retargeting to download seperate audio stream")
                self.has_seperate_audio = True
                self._check_ffmpeg_path()
                args_dict.update({
                    "input": utils.find_absolute_uri(baseurl, media_stream),
                    "output": "merged_audio.ts",
                    "tempdir": args_dict["tempdir"] + "_audio",
                })
                command_save(Namespace(**args_dict), check=self.check)

            elif media_stream.type == "SUBTITLES" and media_stream.autoselect == "YES":
                self.print_info("retargeting to download subtitle stream")
                self.has_subtitle = True
                args_dict.update({
                    "input": utils.find_absolute_uri(baseurl, media_stream),
                    "output": "merged_subtitle.srt",
                    "tempdir": args_dict["tempdir"] + "_subtitle",
                })
                command_save(Namespace(**args_dict), check=self.check)

    def download_in_mutiple_thread(self, segments: m3u8.SegmentList, parsed_links: Tuple[str, str]) -> None:
        """download segments from m3u8.SegmentList object 

        Args:
            segments (m3u8.SegmentList): segments object
            parsed_links (Tuple[str, str]): parsed links
        """
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
                        "uri": utils.find_absolute_uri(parsed_links[1], segment),
                        "key": self._find_key(parsed_links[1], segment),
                        "iv": self._find_iv(segment),
                        "index": processed_ts_index,
                        "retrycount": 0
                    }

                    processed_ts_index += 1
                    executor.submit(self._download_segment_in_thread, segment_dict)

            # retry until all segments are downloaded or reaches the retry limit
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
    
    def _find_key(self, baseurl: Union[str, None], segment: m3u8.Segment) -> Union[str, None]:
        if self.args.key_iv is not None:
            return f"b'{self.args.key_iv.split('==>')[0]}'"

        if segment.key is not None:
            key_absolute_uri = utils.find_absolute_uri(baseurl, segment.key)
            key = b""
            for chunk in self.download_session.get(key_absolute_uri):
                key += chunk
            return f"{key}"
        else:
            return None

    def _find_iv(self, segment: m3u8.Segment) -> Union[str, None]:
        if self.args.key_iv is not None:
            return f"{self.args.key_iv.split('==>')[1]}"

        if segment.key is not None:
            return segment.key.iv.replace("0x", "")
        else:
            return None

    def _download_segment_in_thread(self, segment_dict: dict) -> None:
        
        def _save_json_file(filename: str, segment_dict: dict) -> None:
            # dumping segment info to a json file
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(segment_dict, f, indent=4)
                
        info_filename = f"{self.args.tempdir}/{segment_dict['index']}_info.json"
        _save_json_file(info_filename, segment_dict)

        try:
            self._downloading_core(segment_dict)

        except Exception as e:
            if segment_dict["retrycount"] <= self.args.retry_count:
                # update retrycount on each failed call
                segment_dict.update({"retrycount": segment_dict["retrycount"] + 1})
                _save_json_file(info_filename, segment_dict)
                self.print_info(f"segment {segment_dict['index']} added to retry queue {segment_dict['retrycount']}")
            else:
                print()
                self.print_exception(e)
                console.print("[red bold]VSDownloadError:[/red bold] download failed, re-run the command with [green]--no-cleanup[/green] flag to resume download\n")
                os._exit(1)
                
    def _downloading_core(self, segment_dict: dict) -> None:
        filename = f"{self.args.tempdir}/{segment_dict['index']}.ts"  
        response = self.download_session.get(segment_dict["uri"], stream=True)	
        ts_file_size = int(response.headers.get("Content-Length", 0))

        # spawns tqdm download progess bar for ts segment
        if self.args.verbose:
            ts_file_data = tqdm.tqdm(response.iter_content(self.args.chunk_size), desc=f"{segment_dict['index']}.ts", ncols=0,
                                     total=int(ts_file_size / self.args.chunk_size), leave=False, unit="KB", unit_scale=True, unit_divisor=1024)
        else:
            ts_file_data = response.iter_content(self.args.chunk_size)

        # signal to skip re-downloading of ts file if it exists with original size in local drive
        download_ts = False
        if os.path.isfile(filename):
            if round(os.stat(filename).st_size) != round(ts_file_size):
                download_ts = True
        else:
            download_ts = True

        start = time.perf_counter() # counter to measure somewhat download speed

        # for encrypted ts
        if download_ts and segment_dict["key"] is not None:
            with open(filename, "wb") as f:
                encrypted_ts_data = b""
                for data in ts_file_data:
                    encrypted_ts_data += data

                try:
                    f.write(utils.decrypt_aes_data(encrypted_ts_data, eval(segment_dict["key"]), segment_dict["iv"]))
                except Exception as e:
                    print()
                    self.print_exception(e)
                    console.print(f"[red bold]VSDownloadError:[/red bold] {filename} decryption failed\n")
                    os._exit(1)

        # for non encrypted ts
        elif download_ts:
            with open(filename, "wb") as f:
                for data in ts_file_data:
                    f.write(data)

        # download status sync to tqdm progress bar
        self.process_segments.update(1) # updates tqdm progress bar
        self.merged_file_size += ts_file_size # adds up ts file size to total merged size
        # estimated size = (total downloaded data / downloaded segments count) * total segments
        estimated_size = (self.merged_file_size / self.process_segments.n) * (self.total_ts_files)
        # download speed = ts file size / downloading time
        download_speed = ts_file_size / (time.perf_counter() - start)
        # description format --> total downloaded data / estimated size , download speed
        self.process_segments.set_description(
            f"{utils.convertbytes(self.merged_file_size)[0]}/" +
            f"{utils.convertbytes(estimated_size)[0]}, " +
            f"{utils.convertbytes(download_speed)[0].replace(' ', '')}/s"
        )

    # this function uses binary merge method for merging ts files
    def _ts_merge_task(self, total_ts_files: int) -> None:
        self.print_info(f"\nts file merge task starting in {self.args.timeout} seconds...\n")
        time.sleep(self.args.timeout)

        filename = self.merged_tsfile_path if not self.has_seperate_audio else "merged_video.ts"
        with open(filename, "wb") as f:
            for i in tqdm.trange(1, total_ts_files + 1):
                try:
                    with open(f"{self.args.tempdir}/{i}.ts", "rb") as f2:
                        f.write(f2.read())
                except FileNotFoundError:
                    self._runtime_error(f"{i}.ts file is missing")
                
    def _ffmpeg_covert_task(self) -> None:
        self.print_info(f"\nffmpeg convert task starting in {self.args.timeout} seconds...")
        time.sleep(self.args.timeout)
        
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
            self.print_info(f"temporary merged ts file is saved at {self.merged_tsfile_path}")
            self.print_exception(e)
            self._runtime_error("ts conversion failed")

    def _clean_up_task(self) -> None:
        self.print_info(f"\nclean up task starting in {self.args.timeout} seconds...")
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
            self.print_exception(e)
            self._runtime_error("clean up task failed")
        
    def _runtime_error(self, msg: Optional[str] = "no message specified", code: Optional[int] = 1) -> NoReturn:
        console.print(f"[red bold]VSDownloadError:[/red bold] {msg}")
        if not self.check:
            sys.exit(code)
        else:
            raise RuntimeError(msg)

    def _check_ffmpeg_path(self) -> None:
        if self.args.ffmpeg_path == "ffmpeg" and shutil.which(self.args.ffmpeg_path) is None:
            self._runtime_error("ffmpeg is not installed, visit https://ffmpeg.org/download.html")
        elif self.args.ffmpeg_path != "ffmpeg" and not os.path.isfile(self.args.ffmpeg_path):
            self._runtime_error("ffmpeg is not installed, visit https://ffmpeg.org/download.html")
            
    @staticmethod
    def print_exception(e: Exception) -> None:
        console.print(f"[red bold]{e.__class__.__name__}:[/red bold] {e.__str__()}")
                                
    @staticmethod
    def print_info(msg: str) -> None:
        console.print(f"INFO: {msg}", style="white on blue")

                                        
def command_save(args: Namespace, check: Optional[bool] = False):
    m3u8_downloader = ProcessM3U8(args, check=check)
    
    if not args.input.endswith(".json"):
        parsed_links = m3u8_downloader.parse_link_file()
    else:
        parsed_links = m3u8_downloader.parse_log_json()	

    segments = m3u8_downloader.parse_m3u8(parsed_links)
    print(f"file will be saved at: {args.output}")
    print(f"starting download in {args.threads} thread/s\n")
    m3u8_downloader.download_in_mutiple_thread(segments, parsed_links)
    console.print(f"\nfile downloaded successfully at: [green]{args.output}[/green]")

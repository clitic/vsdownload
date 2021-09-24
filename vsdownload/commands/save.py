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
from concurrent.futures import ThreadPoolExecutor
from . import utils


class ProcessM3U8:

	def __init__(self, args):
		self.args = args
		self.merged_file_size = 0
		self.merged_tsfile_path = os.path.splitext(args.output)[0] + ".ts"
		# check for ffmpeg installation
		if not args.output.endswith(".ts"):
			try:
				subprocess.run([args.ffmpeg_path, "-version"])
			except FileNotFoundError:
				self.runtime_error("ffmpeg is not installed, try using --ffmpeg-path path/to/ffmpeg.exe")
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

	def parse_link_file(self):
		target_url = self.args.input

		if self.args.baseurl is None:
			if target_url.startswith("http"):
				baseurl = utils.find_baseurl_by_urls([target_url], "m3u8")
			else:
				self.runtime_error("-b, --baseurl not set for local m3u8 file.")
		else:
			baseurl = self.args.baseurl

		return target_url, baseurl

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

	def parse_m3u8(self, parsed_links):
		target_url, baseurl = parsed_links

		try:
			print(f"fetching m3u8 content: {target_url}")
			m3u8_file = m3u8.load(target_url, headers=self.headers, http_client=self.http_client).data
			segments = m3u8_file["segments"]

			if segments == []:
				print("m3u8 playlists listed inside m3u8 file:")

				for i, m3u8_playlists in enumerate(m3u8_file["playlists"]):
					print(f"-------------------- {i + 1} --------------------")
					for spec, val in m3u8_playlists["stream_info"].items():
						print(f"{spec}: {val}")

				print()
				selected_playlist = int(input("choose a m3u8 playlist (1, 2, etc.): "))
				print()

				m3u8_playlist_file = m3u8_file["playlists"][selected_playlist - 1]
				m3u8_full_url = urllib.parse.urljoin(baseurl, m3u8_playlist_file["uri"]) if m3u8_playlist_file["uri"].startswith("http") is False else m3u8_playlist_file["uri"]

				print(f"fetching segments from m3u8 playlist: {m3u8_full_url}")
				m3u8_file = m3u8.load(m3u8_full_url, headers=self.headers, http_client=self.http_client).data
				segments = m3u8_file["segments"]
			
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

		with open(self.merged_tsfile_path, "wb") as f:
			for i in tqdm.trange(1, total_ts_files + 1):
				try:
					with open(f"{self.args.tempdir}/{i}.ts", "rb") as f2:
						f.write(f2.read())
				except FileNotFoundError:
					self.runtime_error(f"{i}.ts file is missing")
				
	def _ffmpeg_covert_task(self):
		if not self.args.output.endswith(".ts") :
			print()
			print("running ffmpeg convert task")
			print(f"starting in {self.args.timeout} seconds...")

			try:
				subprocess.run([self.args.ffmpeg_path, "-i", self.merged_tsfile_path, "-c", "copy", self.args.output])
			except Exception as e:
				print(e.__str__())
				print(f"info: temporary merged ts file is saved at {self.merged_tsfile_path}")
				self.runtime_error("ts conversion failed")

	def _clean_up_task(self):
		if self.args.cleanup:
			print()
			print("clean up task")
			print(f"starting in {self.args.timeout} seconds...")
			time.sleep(self.args.timeout)

			try:
				shutil.rmtree(self.args.tempdir)
					
				if not self.args.output.endswith(".ts"):
					os.remove(self.merged_tsfile_path)
			except Exception as e:
				print(e.__str__())
				self.runtime_error("clean up task failed")

	def _download_segment_in_thread(self, parsed_links, segment, process_segments, total_ts_files):
		segment_full_url = urllib.parse.urljoin(parsed_links[1], segment["uri"]) if not segment["uri"].startswith("http") else segment["uri"]
		filename = f"{self.args.tempdir}/{segment['index']}.ts"

		# dumping segment info to a json file
		with open(f"{self.args.tempdir}/{segment['index']}_info.json", "w") as f:
					json.dump({"segment": segment}, f, indent=4)

		try:
			response = self.download_session.get(segment_full_url, stream=True)	
			ts_file_size = int(response.headers.get("Content-Length", 0))
			start = time.perf_counter()

			# skip redownloading of ts file if it exists with original size
			if os.path.isfile(filename):
				if round(os.stat(filename).st_size) != round(ts_file_size):
					with open(filename, "wb") as f:
						for data in response.iter_content(self.args.chunk_size):
							f.write(data)
			else:
				with open(filename, "wb") as f:
					for data in response.iter_content(self.args.chunk_size):
						f.write(data)

		except Exception as e:
			# update retrycount on each failed call
			if segment["retrycount"] <= self.args.retry_count:
				segment["retrycount"] = segment["retrycount"] + 1

				with open(f"{self.args.tempdir}/{segment['index']}_info.json", "w") as f:
					json.dump({"segment": segment}, f, indent=4)

				print(f"info: segment {segment['index']} added to retry queue {segment['retrycount']}")
				return 1
			else:
				print("\nerror: download failed\n")
				print(e.__str__())
				os._exit(1)

		# download status sync
		process_segments.update(1)
		self.merged_file_size += ts_file_size
		estimated_size = (self.merged_file_size / process_segments.n) * (total_ts_files)
		download_speed = ts_file_size / (time.perf_counter() - start)
		process_segments.set_description(f"{utils.convertbytes(self.merged_file_size)[0]}/{utils.convertbytes(estimated_size)[0]}, " + 
										 f"{utils.convertbytes(download_speed)[0].replace(' ', '')}/s")

	def download_in_mutiple_thread(self, segments, parsed_links):
		if os.path.exists(self.args.tempdir) and self.args.cleanup:
			shutil.rmtree(self.args.tempdir)
			os.mkdir(self.args.tempdir)

		total_ts_files = len(segments)
		processed_ts_index = 1
		
		with tqdm.tqdm(total=total_ts_files, desc="0 KB/0 KB, 0KB/s", unit="segment") as process_segments:
			with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
				for segment_dict in segments:
					segment_dict["index"] = processed_ts_index
					segment_dict["retrycount"] = 0
					processed_ts_index += 1
					executor.submit(self._download_segment_in_thread, parsed_links, segment_dict, process_segments, total_ts_files)

			# retry pool
			while process_segments.n != total_ts_files:
				with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
					for i in range(1, total_ts_files + 1):
						with open(f"{self.args.tempdir}/{i}_info.json") as f:
							segment_dict = json.load(f)["segment"]
						
						if segment_dict["retrycount"] != 0 and segment_dict["retrycount"] <= self.args.retry_count:
							executor.submit(self._download_segment_in_thread, parsed_links, segment_dict, process_segments, total_ts_files)
						elif segment_dict["retrycount"] >= self.args.retry_count:
							break
						
		self._ts_merge_task(total_ts_files)
		self._ffmpeg_covert_task()
		self._clean_up_task()	

def command_save(args):
	process_m3u8_c = ProcessM3U8(args)
	
	if args.input.endswith(".json"):
		parsed_links = process_m3u8_c.parse_log_json()	
	else:
		parsed_links = process_m3u8_c.parse_link_file()

	print(f"baseurl is set to: {parsed_links[1]}")
	segments = process_m3u8_c.parse_m3u8(parsed_links)
	print(f"file will be saved at: {args.output}")
	print(f"starting download in {args.threads} thread/s\n")
	process_m3u8_c.download_in_mutiple_thread(segments, parsed_links)	
	print(f"\nfile downloaded successfully at: {args.output}")

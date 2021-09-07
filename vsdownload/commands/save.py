import requests
import tqdm
import json
import sys
import os
import shutil
import subprocess
import time
import urllib.parse
import m3u8
from . import utils


class process_m3u8:
	def __init__(self, args):
		self.args = args
		self.merged_file_size = 0
		self.processed_ts_counts = 1
		self.merged_tsfile_path = os.path.splitext(args.output)[0] + ".ts"

	@staticmethod
	def runtime_error(msg="no message specified", code=1):
		print(f"error: {msg}")
		sys.exit(code)

	def parse_link_file(self):
		target_url = self.args.input

		if self.args.blob is None:
			if target_url.startswith("http"):
				blob = utils.find_blob_by_urls([target_url], "m3u8")
			
			else:
				self.runtime_error("-b, --blob not set for local file, basically it is endpoint url for all segments.")

		else:
			blob = self.args.blob

		return target_url, blob

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
		
		if self.args.blob is None:
			blob = json_data["blob"]
		else:
			blob = self.args.blob
		
		return target_url, blob

	def parse_m3u8(self, parsed_links):
		target_url, blob = parsed_links

		try:
			print(f"resolving url/file: {target_url}")
			m3u8_file = m3u8.load(target_url).data
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
				m3u8_full_url = urllib.parse.urljoin(blob, m3u8_playlist_file["uri"]) if m3u8_playlist_file["uri"].startswith("http") is False else m3u8_playlist_file["uri"]

				print(f"resolving m3u8 playlist url: {m3u8_full_url}")
				m3u8_file = m3u8.load(m3u8_full_url).data
				segments = m3u8_file["segments"]
			
			return segments

		except:
			self.runtime_error("bad m3u8 url/file")

	def _ts_merge_task(self, total_ts_files):
		print()
		print("ts files merge task")
		print(f"starting in {self.args.timeout} seconds...")
		time.sleep(self.args.timeout)
		print()

		try:
			with open(self.merged_tsfile_path, "wb") as f:
				for i in tqdm.trange(1, total_ts_files + 1):
					with open(f"{self.args.tempdir}/{i}.ts", "rb") as f2:
						f.write(f2.read())

		except FileNotFoundError:
			self.runtime_error("some ts files are missing")
			
	def _ffmpeg_covert_task(self):
		if self.args.output.endswith(".ts") is False:
			print()
			print("running ffmpeg convert task")
			print(f"starting in {self.args.timeout} seconds...")

			try:
				subprocess.run([self.args.ffmpeg_path, "-i", self.merged_tsfile_path, "-c", "copy", self.args.output])
			except:
				print(f"info: temporary merged ts file is saved at {self.merged_tsfile_path}")
				self.runtime_error("ts conversion failed")

	def _clean_up_task(self):
		print()
		print("clean up task")
		print(f"starting in {self.args.timeout} seconds...")
		time.sleep(self.args.timeout)

		try:
			if self.args.threads < 1:
				shutil.rmtree(self.args.tempdir)
				
			if self.args.output.endswith(".ts") is False:
				os.remove(self.merged_tsfile_path)
		except:
			self.runtime_error("clean up task failed")

	def _segment_stream(self, segment, parsed_links):
		blob = parsed_links[1]
		segment_full_url = urllib.parse.urljoin(blob, segment["uri"]) if segment["uri"].startswith("http") is False else segment["uri"]

		if self.args.user_agent is None:
			response = requests.get(segment_full_url, stream=True)
		else:
			headers = {"User-Agent": self.args.user_agent}
			response = requests.get(segment_full_url, stream=True, headers=headers)
			
		ts_file_size = int(response.headers.get("Content-Length", 0))
		self.merged_file_size += ts_file_size
		progress = response.iter_content(self.args.chunk_size)

		return progress, ts_file_size

	def _download_status_sync(self, total_ts_files, ts_file_size, start, process_segments):
		downloaded_data = self.merged_file_size
		estimated_size = (self.merged_file_size / self.processed_ts_counts) * (total_ts_files)
		
		try:
			download_speed = (ts_file_size / (time.time() - start)) * self.args.threads
		except ZeroDivisionError:
			download_speed = 0
		
		process_segments.set_description(f"{utils.convertbytes(downloaded_data)[0]}/{utils.convertbytes(estimated_size)[0]}, {utils.convertbytes(download_speed)[0].replace(' ', '')}/s")
		self.processed_ts_counts += 1

	def download_in_single_thread(self, segments, parsed_links):
		process_segments = tqdm.tqdm(segments, desc="0 KB/0 KB, 0KB/s", unit="segment")
		total_ts_files = len(segments)

		with open(self.merged_tsfile_path, "wb") as f:
			for segment in process_segments:
				try:
					segment_stream, ts_file_size = self._segment_stream(segment, parsed_links)
					start = time.time()
					for data in segment_stream:
						f.write(data)

				except:
					print("\n\n")
					self.runtime_error("download failed")
				
				self._download_status_sync(total_ts_files, ts_file_size, start, process_segments)

		if self.args.output.endswith(".ts") is False:
			self._ffmpeg_covert_task()
			self._clean_up_task()

	@utils.threaded
	def _download_segment_in_thread(self, parsed_links, segment, process_segments, total_ts_files):
		try:
			segment_stream, ts_file_size = self._segment_stream(segment, parsed_links)
			start = time.time()
			with open(f"{self.args.tempdir}/{segment['index']}.ts", "wb") as f:
				for data in segment_stream:
					f.write(data)

		except:
			print("\nerror: download failed\n")
			os._exit(1)

		process_segments.update(1)
		self._download_status_sync(total_ts_files, ts_file_size, start, process_segments)

	def download_in_mutiple_thread(self, segments, parsed_links):
		if os.path.exists(self.args.tempdir):
			shutil.rmtree(self.args.tempdir)

		os.mkdir(self.args.tempdir)

		total_ts_files = len(segments)
		processed_ts_index = 1

		with tqdm.tqdm(total=total_ts_files, desc="0 KB/0 KB, 0KB/s", unit="segment") as process_segments:
			while segments != []:
				active_threads = []

				for _ in range(self.args.threads):
					try:
						segments_dict = segments.pop(0)
					except IndexError:
						break

					segments_dict["index"] = processed_ts_index
					processed_ts_index += 1
					current_thread = self._download_segment_in_thread(parsed_links, segments_dict, process_segments, total_ts_files)
					active_threads.append(current_thread)
				
				try:
					for current_thread in active_threads:
						current_thread.join()

				except KeyboardInterrupt:
					print("\n\nerror: download failed\n")
					os._exit(1)

			while process_segments.n != total_ts_files:
				time.sleep(self.args.timeout)

		self._ts_merge_task(total_ts_files)
		self._ffmpeg_covert_task()
		self._clean_up_task()	

def command_save(args):
	process_m3u8_c = process_m3u8(args)
	
	if args.input.endswith(".json"):
		parsed_links = process_m3u8_c.parse_log_json()	
	else:
		parsed_links = process_m3u8_c.parse_link_file()

	print(f"base endpoint is set to: {parsed_links[1]}")

	segments = process_m3u8_c.parse_m3u8(parsed_links)

	print(f"file will be saved at: {args.output}")
	print(f"starting download in {args.threads} thread/s")
	print()

	if args.threads == 1:
		process_m3u8_c.download_in_single_thread(segments, parsed_links)
	else:
		process_m3u8_c.download_in_mutiple_thread(segments, parsed_links)

	print()		
	print(f"file downloaded successfully at: {args.output}")

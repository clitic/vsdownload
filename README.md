# VSDownload - Video Stream (M3U8) Downloader

command line program to download hls video streams from websites, m3u8 files and urls. [What is m3u8 ?](https://en.wikipedia.org/wiki/M3U)

<p align="center">
  a compact lightweight m3u8 downloader
</p>

<p align="center">
  <img src="https://img.shields.io/badge/dynamic/json?style=flat-square&maxAge=86400&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fvsdownload">
  <img src="https://img.shields.io/pypi/v/vsdownload?style=flat-square">
  <img src="https://img.shields.io/badge/python-%3E=_3.6-green?style=flat-square"/>
  <img src="https://img.shields.io/github/license/clitic/vsdownload?style=flat-square">
  <img src="https://img.shields.io/github/repo-size/clitic/vsdownload?style=flat-square">
  <img src="https://img.shields.io/tokei/lines/github/clitic/vsdownload?style=flat-square">
</p>

<p align="center">
  <a href="#Installations">Installations</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#Usage">Usage</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/clitic/vsdownload/main/images/vsdownload.gif">
</p>

## Features Implemented

- [x] auto binary merge for ts segments
- [x] auto decrypt for aes standard cbc encrypted playlists (beta)
- [x] auto mux for seperate video, audio and subtitle (webvtt) stream
- [x] capturing m3u8 links and urls from a website
- [x] custom headers, proxies, key and iv
- [x] downloading in multiple threads
- [x] ffmpeg conversion integration
- [x] gui support
- [x] master m3u8 playlist parsing
- [x] platform independent
- [x] realtime file size prediction (arithmetic mean) and downloading speed
- [x] resume and retry support
- [ ] supports live stream download

## Important Declaration

If you are distributing downloaded video streams, first ensure that you have rights for those video streams or files.

## Installations

Requires*

- [python3.6+](https://www.python.org/downloads) and [pip](https://pip.pypa.io/en/stable/installation)
- [ffmpeg](https://www.ffmpeg.org/download.html) (optional)
- [chrome](https://www.google.com/chrome/) and [chrome web driver](https://chromedriver.chromium.org/downloads) (optional)

```bash
pip install vsdownload
```

Or install from github repository.

```bash
pip install https://github.com/clitic/vsdownload/archive/main.zip
```

Or you can also find a windows [executable](https://github.com/clitic/vsdownload/releases/download/v1.1.21/vsdownload.exe) / [gui wrapper](https://github.com/clitic/vsdownload/releases/download/v1.1.21/vsdownload_gui.zip) from [releases](https://github.com/clitic/vsdownload/releases).

## Usage

- [How to get m3u8 file link ?](https://github.com/clitic/vsdownload/blob/main/docs/FAQs.md#How+to+get+m3u8+file+link+?)

- Capturing m3u8 files from website and downloading hls streams

```bash
vsdownload capture <website url> --driver <driver path>
vsdownload save log.json
```

- Downloading hls video streams from m3u8 files

```bash
vsdownload save <m3u8 url or file> -o video.mp4
```

> In **-o/--output** flag, any ffmpeg supported extension could be provided <br> Add **--no-cleanup** flag to use resume capabilities

- [CLI-API.md](docs/CLI-API.md)
- [FAQs.md](docs/FAQs.md)

## GUI Wrapper

<p align="center">
  <img src="https://raw.githubusercontent.com/clitic/vsdownload/main/images/gui_wrapper.jpg">
</p>

To use gui wrapper, first install PyQt6 and then run **vsdownload-gui**

```bash
$ pip install PyQt6
$ vsdownload-gui
```

## Scripting And Automation

You can also integrate vsdownload save and capture command in any python program. This is useful when you have to automate or create sub website m3u8 downloaders. First you can find or parse the m3u8 uri from a website then call `vsdownload.save()` function in order to download it.

- save command function

```python
from vsdownload import vsdownload

vsdownload.save("http://videoserver.com/playlist.m3u8", output="merged.mp4")
```

- capture and save command functions

```python
from vsdownload import vsdownload

log_file = "stream_log.json"

vsdownload.capture("http://streamingsite.com/stream.html", "chromedriver.exe", output=log_file)
vsdownload.save(log_file, output="merged.mp4")
```

- calling vsdownload through subprocess

```python
import subprocess

command_args = [
  "vsdownload", # command
  "save", # sub command
  "http://videoserver.com/playlist.m3u8", # input
  "-o", # extra options
  "a.mp4" # output file
]

try:
  subprocess.run(command_args, check=True)
except subprocess.CalledProcessError as e:
  print(f"error code: {e.returncode}")
```

## License

&copy; 2021-22 clitic

This repository is licensed under the MIT license. See LICENSE for details.

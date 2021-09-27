# VS Download - Video Stream Download

command line program to download hls video streams from websites, m3u8 files and urls.

<p align="center">
  a compact lightweight m3u8 downloader
</p>

<p align="center">
  <a href="https://pypi.org/project/vsdownload/"><img src="https://pepy.tech/badge/vsdownload" alt="Total Downloads"></a>
  <a href="https://www.python.org/downloads/" title="Python Version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
  <a href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <a href="https://pypi.org/project/vsdownload/"><img src="https://badge.fury.io/py/vsdownload.svg" alt="PyPi Package Version"></a>
  <a href="https://github.com/360modder/vsdownload"><img src="https://img.shields.io/github/repo-size/360modder/vsdownload.svg" alt="Repository Size"></a>
</p>

<p align="center">
  <a href="#Installations">Installations</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#Usage">Usage</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/360modder/vsdownload/master/images/vsdownload.gif">
</p>

## Features Implemented

- [x] auto binary merge for ts segments
- [x] auto decrypt for aes standard cbc encrypted playlists (beta)
- [x] auto mux for seperate video, audio and subtitle (webvtt) stream
- [x] capturing m3u8 links and urls from a website
- [x] custom headers, proxies, key and iv
- [x] downloading in multiple threads
- [x] ffmpeg conversion integration
- [x] master m3u8 playlist parsing
- [x] platform independent
- [x] realtime file size prediction (arithmetic mean) and download speed
- [x] resume support
- [x] retry on error

> Create an issuse to request a new feature

## Important Declaration

If you are distributing downloaded video streams, first ensure that you have rights for those video streams or files.

## Installations

Requires*

- [python3.6+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/)
- [chrome](https://www.google.com/chrome/) and [chrome web driver](https://chromedriver.chromium.org/downloads) (as per use cases)
- [ffmpeg](https://www.ffmpeg.org/download.html) (as per use cases)

```bash
pip install vsdownload
```

Or install from github repository.

```bash
pip install https://github.com/360modder/vsdownload/archive/master.zip
```

Or you can also find a windows [executable](https://github.com/360modder/vsdownload/releases/download/v1.0.98/vsdownload.exe) from [releases](https://github.com/360modder/vsdownload/releases).

## Usage

- Capturing m3u8 files from website and downloading hls streams

```bash
vsdownload capture <website url> --driver <driver path>
vsdownload save log.json
```

- Downloading hls video streams from m3u8 files

```bash
vsdownload save <m3u8 url or file> -o video.ts
```

> Add **--no-cleanup** flag to use resume capabilities

## How to convert .ts to .mp4, .mkv etc. ?

First download and install [ffmpeg](https://www.ffmpeg.org/download.html) and then in output flag specify your desired format.

```bash
vsdownload save <m3u8 url or file> -o video.mp4
```

If ffmpeg is not in system binary path then use **--ffmpeg-path** flag.


```bash
vsdownload save <m3u8 url or file> --ffmpeg-path <path to ffmpeg binary> -o video.mp4
```

## How to speed up downloading speed ?

Downloading ts files with more multiple worker threads would be a good option and also using a higher chunk size will reduce the file i/o operations. vsdownload can handle those things by using some flags.

Downloading m3u8 files with 16 threads with 4k chunk size.

```bash
vsdownload save <m3u8 url or file> --chunk-size 4096 -t 16 -o video.ts
```

## Downloaded hls stream size in bytes and corrupted ?

This problem arises when vsdownload makes get request to ts file and it returns a bad response body which results in corrupted downloads.

This error maybe caused by incorrect segment url which is auto parsed by vsdownload. You can manually override it by following the given steps. 

Steps resolve this error:

1. Check for m3u8 uri and other ts files uri/s from your browser's network logs or use **vsdownload capture** command. you will notice a comman url attached to very ts file uri, then note it down as **baseurl**.

```
Example:

1. https://xyz.in/283678-293/stream-hls/stream_0_high.m3u8
2. https://xyz.in/283678-293/stream-hls/stream_0_high_01.ts
5. https://xyz.in/283678-293/stream-hls/stream_0_high_02.ts
4. https://xyz.in/283678-293/stream-hls/stream_0_high_03.ts

Baseurl (comman url / base endpoint): https://xyz.in/283678-293/stream-hls/
```

2. After getting a baseurl try to download stream by using this command.

```bash
vsdownload save <m3u8 url or file> -b <baseurl> -o video.ts
```

```bash
Example:

vsdownload save https://xyz.in/283678-293/stream-hls/stream_0_high.m3u8 -b https://xyz.in/283678-293/stream-hls/ -o video.ts
```

3. If stream doesn't download till now then you can check few options given below.

Some extra things to try for websites which don't make their hls streams publicly open.

1. Maintain a connection to server by playing stream in browser or from any other means.
2. Check for maximum supported parallel connections from server. If it can use more than 1 connection, then streams maybe downloaded by following the above steps.
3. Use **--proxy-address** flag.

## Documentations

- [CLI-API.md](CLI-API.md)
- [CHANGELOG.md](CHANGELOG.md)

## License

© 2021 360modder

This repository is licensed under the MIT license. See LICENSE for details.

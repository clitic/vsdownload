# VSDownload Changelog (DD/MM/YYYY)

## 1.1.21 (06/11/2021)

Features:

- Verbose downloading output
- Added `-m/--max-quality` option
- Colorful console outputs
- Optimized downloads and gui wrapper
- Raises RuntimeError on calling `vsdownload.save()`

Changes:

- `-o` option alais added to capture command `--output` option
- Now version checking is only done by `--version` flag only

Bug Fixes:

- Timeout for ffmpeg convert task
- Explicit command copy to clipboard in gui wrapper

## 1.1.02 (10/10/2021)

Features:

- More support for scripting and automation

Bug Fixes:

- gui window close on clicking execute button in linux

## 1.1.0 (07/10/2021)

Features:

- Added gui wrapper

## 1.0.98 (27/09/2021)

Features:

- Now capable to download seperate video, audio and subtitle (webvtt) stream
- Beta support for aes standard cbc encrypted playlists

Changes:

- More clean checking of ffmpeg path
- `ProcessM3U8.parse_m3u8()` returns `m3u8.PlaylistList`
- Now using m3u8's absolute uri and *--baseurl* is set to None by default
- `--retry-count` is set to 10 by default

## 1.0.76 (24/09/2021)

Features:

- Now supports resumable downloading
- Retry support on encountering error
- Use custom headers configration json file
- Use custom http and https proxies
- Pre ffmpeg path check

Changes:

- No single threaded downloads, merged with thread pool executor with default as 5 workers
- Now using a requests session for making a get request
- Now KeyboardInterrupt is not handled, you have to kill the running script manually
- `--blob` option renamed to `--baseurl`
- `--user-agent` option removed

Bug Fixes:

- Unnecessary clean up task for single threaded downloads

Added:

- Makefile to deploy a windows executable

## 1.0.52 (29/07/2021)

Features:

- Typer CLI instead of argsparse 
- Improved downloading with multiple threads
- ffmpeg ts conversion integration
- Download speed meter
- Data console output for **vsdownload capture** command

Fixed:

- Exit from a multithreaded download

## 1.0.0 (04/07/2021)

Features:

- Initial release

# `vsdownload`

command line program to download hls video streams from websites, m3u8 files and urls

**Usage**:

```console
$ vsdownload [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: show current version of vsdownload
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `capture`: capture m3u8 urls from a website
* `save`: download m3u8 stream from m3u8 url or file

## `vsdownload capture`

capture m3u8 urls from a website

**Usage**:

```console
$ vsdownload capture [OPTIONS] URL
```

**Arguments**:

* `URL`: website url to target  [required]

**Options**:

* `-o, --output mysite_log.json`: output website m3u8 capture logs in which path  [default: log.json]
* `--driver chromedriver.exe`: path of chrome driver for selenium
* `--scan-ext m3u8/ts/mp4`: scan network logs until --scan-ext extension is found in any one of the request url  [default: ts]
* `--baseurl / --no-baseurl`: detect baseurl (not recommended)  [default: False]
* `--help`: Show this message and exit.

## `vsdownload save`

download m3u8 stream from m3u8 url or file

**Usage**:

```console
$ vsdownload save [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: url|.m3u8|log.json  [required]

**Options**:

* `-o, --output merged.ts/merged.mp4/merged.mkv`: path for output of downloaded video stream file  [default: merged.ts]
* `--cleanup / --no-cleanup`: delete temporary downloaded segments, add --no-cleanup flag to use resume capabilities  [default: True]
* `-m, --max-quality`: auto select highest quality sub m3u8 playlist  [default: False]
* `-v, --verbose`: verbose downloading outputs and logs  [default: False]
* `-b, --baseurl http://videoserver.com/`: base url for all segments, usally needed for local m3u8 file
* `-t, --threads 1-16`: max thread count for parallel threads to download segments  [default: 5]
* `--chunk-size INTEGER`: chunk size for downloading ts files (in kilobytes)  [default: 1024]
* `--headers headers.json`: path of header defining json file which will update headers
* `--decrypt / --no-decrypt`: auto decrypt ts files  [default: True]
* `--key-iv key==>iv`: custom decryption key and iv (key==>iv)
* `--proxy-address http://xx`: http or https proxy address to use
* `--ffmpeg-path c:\ffmpeg\bin\ffmpeg.exe`: path of ffmpeg binary  [default: ffmpeg]
* `--tempdir directory`: path of directory for saving temporary files while downloading  [default: temptsfiles]
* `--retry-count INTEGER`: retry count for downloading segment  [default: 10]
* `--timeout time`: waiting time for post tasks to perform after downloading (in seconds)  [default: 5]
* `--pre-select INTEGER`: pre select a url from log.json file
* `--help`: Show this message and exit.

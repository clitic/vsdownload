# `vsdownload`

command line extension to download hls video streams from websites, m3u8 files and urls

**Usage**:

```console
$ vsdownload [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: show installed version of vsdownload
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `capture`: capture m3u8 urls from a website
* `save`: download and save ts file from m3u8 url or...

## `vsdownload capture`

capture m3u8 urls from a website

**Usage**:

```console
$ vsdownload capture [OPTIONS] URL
```

**Arguments**:

* `URL`: website url to target  [required]

**Options**:

* `--output TEXT`: output website m3u8 capture logs in which path  [default: log.json]
* `--driver TEXT`: path of chrome driver which selenium going to use
* `--scan-ext TEXT`: scan network logs until --scan-ext extension is found in any of url  [default: ts]
* `--help`: Show this message and exit.

## `vsdownload save`

download and save ts file from m3u8 url or file

**Usage**:

```console
$ vsdownload save [OPTIONS] INPUT
```

**Arguments**:

* `INPUT`: url | .m3u8 | log.json  [required]

**Options**:

* `-o, --output TEXT`: path for output for downloaded ts file  [default: merged.ts]
* `-t, --threads INTEGER`: download ts files in multiple threads  [default: 1]
* `-b, --blob TEXT`: specific site blob which is used for making a full url from m3u8 segments uri
* `--user-agent TEXT`: by default make a request to url without user agent header
* `--chunk-size INTEGER`: chunk size for downloading ts files in kilobytes  [default: 1024]
* `--ffmpeg-path TEXT`: path of ffmpeg binary  [default: ffmpeg]
* `--tempdir TEXT`: directory for saving temporary ts files when downloading in mutiple threads  [default: temptsfiles]
* `--timeout INTEGER`: when using threads waiting time for tasks to perform in seconds  [default: 5]
* `--pre-select INTEGER`: pre select a url from log.json file
* `--help`: Show this message and exit.

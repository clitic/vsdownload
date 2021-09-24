# CHANGELOG.md

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

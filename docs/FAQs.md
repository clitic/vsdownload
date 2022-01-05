# FAQs

## How to get m3u8 file link ?

Open your browser and visit the website which streams m3u8 media. When video get starts playing right click and inspect the webpage. Go to **Network** tab and filter m3u8 extension and copy the master or first m3u8 file link. [Read More](https://gist.github.com/tzmartin/fb1f4a8e95ef5fb79596bd4719671b5d)

<p align="center">
  <img src="https://camo.githubusercontent.com/ac935fd5ff9bdd6af30e8a3cc59eca0d836847b021762658d782d56b0dd9f0a5/68747470733a2f2f6d6f6e6f736e61702e636f6d2f66696c652f7330685846647a4b4a6e77793376323179494a367046314673673054477a2e706e67">
</p>

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

1. http://videoserver.com/playlist.m3u8
2. http://videoserver.com/stream_0.ts
3. http://videoserver.com/stream_1.ts
4. http://videoserver.com/stream_2.ts

Baseurl (comman url / base endpoint): http://videoserver.com/
```

2. After getting a baseurl try to download stream by using this command.

```bash
vsdownload save <m3u8 url or file> -b <baseurl> -o video.ts
```

```bash
Example:

vsdownload save http://videoserver.com/playlist.m3u8 -b http://videoserver.com/ -o video.ts
```

3. If stream doesn't download till now then you can check few options given below.

Some extra things to try for websites which don't make their hls streams publicly open.

1. Maintain a connection to server by playing stream in browser or from any other means.
2. Check for maximum supported parallel connections from server. If it can use more than 1 connection, then streams maybe downloaded by following the above steps.
3. Use **--proxy-address** flag.

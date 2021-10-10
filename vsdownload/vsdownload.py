import typer
from argparse import Namespace
from typing import Optional
from .commands.capture import command_capture
from .commands.save import command_save


__version__ = "1.1.02"
app = typer.Typer(name="vsdownload", help="command line program to download hls video streams from websites, m3u8 files and urls")


def version_callback(value: bool):
    if value:
        typer.echo(f"vsdownload v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, help="show current version of vsdownload")):
    pass

@app.command(name="capture", help="capture m3u8 urls from a website")
def call_capture(
        url: str = typer.Argument(..., help="website url to target"),
        output: str = typer.Option("log.json", help="output website m3u8 capture logs in which path", metavar="mysite_log.json"),
        driver: str = typer.Option(None, help=f"path of chrome driver for selenium", metavar="chromedriver.exe"),
        scan_ext: str = typer.Option("ts", help="scan network logs until --scan-ext extension is found in any one of the request url", metavar="m3u8/ts/mp4"),
        baseurl: bool = typer.Option(False, help="detect baseurl (not recommended)")
    ):
    command_capture(Namespace(**locals()))

@app.command(name="save", help="download m3u8 stream from m3u8 url or file")
def call_save(
        input: str = typer.Argument(..., help="url|.m3u8|log.json"),
        output: str = typer.Option("merged.ts", "--output", "-o", help="path for output of downloaded video stream file", metavar="merged.ts/merged.mp4/merged.mkv"),
        cleanup: bool = typer.Option(True, help="delete temporary downloaded segments, add --no-cleanup flag to use resume capabilities"),
        baseurl: str = typer.Option(None, "--baseurl", "-b", help="base url for all segments, usally needed for local m3u8 file", metavar="http://videoserver.com/", show_default=False),
        threads: int = typer.Option(5, "--threads", "-t", help="max thread count for parallel threads to download segments", metavar="1-32", min=1, max=32),
        chunk_size: int = typer.Option(1024, help="chunk size for downloading ts files (in kilobytes)"),
        headers: str = typer.Option(None, help="path of header defining json file which will update headers", metavar="headers.json", show_default=False),
        key_iv: str = typer.Option(None, help="custom decryption key and iv (key==>iv)", metavar="key==>iv", show_default=False),
        proxy_address: str = typer.Option(None, help="http or https proxy address to use", metavar="http://xx", show_default=False),
        ffmpeg_path: str = typer.Option("ffmpeg", help="path of ffmpeg binary", metavar="c:\\ffmpeg\\bin\\ffmpeg.exe"),
        tempdir: str = typer.Option("temptsfiles", help="path of directory for saving temporary files while downloading", metavar="directory"),
        retry_count: int = typer.Option(10, help="retry count for downloading segment"),
        timeout: int = typer.Option(5, help="waiting time for post tasks to perform after downloading (in seconds)", metavar="time"),
        pre_select: int = typer.Option(None, help="pre select a url from log.json file", show_default=False)
    ):
    command_save(Namespace(**locals()))
        
def capture(
        url: str = ..., output: str = "log.json", driver: str = None, scan_ext: str = "ts", baseurl: bool = False
    ):

    if url is ...:
        raise NotImplementedError("cannot proceed without website url")
    
    if driver is None:
        raise NotImplementedError("cannot proceed without chromedriver path")

    command_capture(Namespace(**locals()))

def save(
        input: str = ..., output: str = "merged.ts", cleanup: bool = True, baseurl: str = None, threads: int = 5, chunk_size: int = 1024, headers: str = None, key_iv: str = None,
        proxy_address: str = None, ffmpeg_path: str = "ffmpeg", tempdir: str = "temptsfiles", retry_count: int = 10, timeout: int = 5, pre_select: int = None
    ):

    if locals()["input"] is ...:
        raise NotImplementedError("cannot proceed without input")

    command_save(Namespace(**locals()))


if __name__ == "__main__":
    app()

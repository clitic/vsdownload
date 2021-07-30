import typer
from argparse import Namespace
from typing import Optional


# some test commands (root)
# python -m vsdownload.vsdownload --help
# python -m vsdownload.vsdownload save https://multiplatform-f.akamaihd.net/i/multi/will/bunny/big_buck_bunny_,640x360_400,640x360_700,640x360_1000,950x540_1500,.f4v.csmil/index_0_av.m3u8 -t 5

__version__ = "1.0.52"
app = typer.Typer(name="vsdownload", help="command line extension to download hls video streams from websites, m3u8 files and urls")


def version_callback(value: bool):
    if value:
        typer.echo(f"vsdownload v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, help="show installed version of vsdownload")):
    pass

@app.command(help="capture m3u8 urls from a website")
def capture(url: str = typer.Argument(..., help="website url to target"),
            output: str = typer.Option("log.json", help="output website m3u8 capture logs in which path"),
            driver: str = typer.Option(None, help=f"path of chrome driver which selenium going to use"),
            scan_ext: str = typer.Option("ts", help="scan network logs until --scan-ext extension is found in any of url")):
    from .commands import capture
    args = Namespace(**locals()) 
    capture.command_capture(args)

@app.command(help="download and save ts file from m3u8 url or file")
def save(input: str = typer.Argument(..., help="url | .m3u8 | log.json"),
        output: str = typer.Option("merged.ts", "--output", "-o", help="path for output for downloaded ts file"),
        threads: int = typer.Option(1, "--threads", "-t", help="download ts files in multiple threads"),
        blob: str = typer.Option(None, "--blob", "-b", help="specific site blob which is used for making a full url from m3u8 segments uri"),
        user_agent: str = typer.Option(None, help="by default make a request to url without user agent header"),
        chunk_size: int = typer.Option(1024, help="chunk size for downloading ts files in kilobytes"),
        ffmpeg_path: str = typer.Option("ffmpeg", help="path of ffmpeg binary"),
        tempdir: str = typer.Option("temptsfiles", help="directory for saving temporary ts files when downloading in mutiple threads"),
        timeout: int = typer.Option(5, help="when using threads waiting time for tasks to perform in seconds"),
        pre_select: int = typer.Option(None, help="pre select a url from log.json file")):
    from .commands import save
    args = Namespace(**locals()) 
    save.command_save(args)

def console_script():
    app()
    
if __name__ == "__main__":
    app()

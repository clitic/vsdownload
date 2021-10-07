import os
import sys
import re
import pathlib
from setuptools import setup


def get_version() -> str:
    """Get __version__ from vsdownload.py file."""
    version_file = os.path.join(os.path.dirname(__file__), "vsdownload", "vsdownload.py")
    version_file_data = open(version_file, "rt", encoding="utf-8").read()
    version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
    try:
        version = re.findall(version_regex, version_file_data, re.M)[0]
        return version
    except IndexError:
        raise ValueError(f"Unable to find version string in {version_file}.")


assert sys.version_info >= (3, 6, 0), "vsdownload requires Python 3.6+"

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open("requirements.txt") as f:
    REQUIREMENTS = [req.replace("\n", "") for req in f.readlines()]

setup(
    name="vsdownload",
    version=get_version(),
    description="command line program to download hls video streams from websites, m3u8 files and urls",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["m3u8", "ts", "video", "stream", "downloader", "m3u8downloader"],
    url="https://github.com/360modder/vsdownload.git",
    author="360modder",
    author_email="apoorv9450@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    packages=["vsdownload", "vsdownload/commands"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
    "console_scripts": [
        'vsdownload=vsdownload.vsdownload:console_script',
        'vsdownload-gui=vsdownload.vsdownload_gui_wrapper:console_script',
    ]}
)        

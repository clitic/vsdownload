"""
some test commands

help:
python main.py --help

normal downloading:
python main.py save https://multiplatform-f.akamaihd.net/i/multi/will/bunny/big_buck_bunny_,640x360_400,640x360_700,640x360_1000,950x540_1500,.f4v.csmil/index_0_av.m3u8

resumable downloading:
python main.py save --no-cleanup https://multiplatform-f.akamaihd.net/i/multi/will/bunny/big_buck_bunny_,640x360_400,640x360_700,640x360_1000,950x540_1500,.f4v.csmil/index_0_av.m3u8

variant playlist:
python main.py save https://multiplatform-f.akamaihd.net/i/multi/will/bunny/big_buck_bunny_,640x360_400,640x360_700,640x360_1000,950x540_1500,.f4v.csmil/master.m3u8

encrypted playlist:
python main.py save https://vod8.wenshibaowenbei.com/20210628/g4yNLlI7/index.m3u8
"""

from vsdownload.vsdownload import app

app()

import inspect
from . import vsdownload

def get_command_callargs(command_name: str):
    """get callargs from a vsdownload function"""
    return inspect.getcallargs(eval(f"vsdownload.{command_name}"))

def get_version():
    """get the vsdownload version"""
    return vsdownload.__version__

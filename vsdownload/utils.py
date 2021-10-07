import inspect
from . import vsdownload

def get_command_callargs(command_name):
    return inspect.getcallargs(eval(f"vsdownload.{command_name}"))

def get_version():
    return vsdownload.__version__

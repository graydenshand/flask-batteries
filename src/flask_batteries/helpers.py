import os
from .config import PATH_TO_VENV, TAB


def pip():
    """
    Return the path to the `pip` executable within a virtual environment.
    """
    path_to_venv = os.environ.get("PATH_TO_VENV", "venv")
    if os.name != "nt":
        # Posix
        return os.path.join(path_to_venv, "bin", "pip")
    else:
        # Windows
        return os.path.join(path_to_venv, "Scripts", "pip")


def activate():
    """
    Return the path to the `activate` shell script within a virtual environment.
    """
    path_to_venv = os.environ.get("PATH_TO_VENV", "venv")
    if os.name != "nt":
        # Posix
        return os.path.join(path_to_venv, "bin", "activate")
    else:
        # Windows
        return os.path.join(path_to_venv, "Scripts", "activate.bat")

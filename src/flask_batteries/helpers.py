import os
from .config import PATH_TO_VENV, TAB
import re


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


def env_var(key, val):
    """
    CROSS PLATFORM
    Produce a string to declare an environment variable in the virtual env activate script
    """
    if os.name != "nt":
        return f"export {key}={val}"
    else:
        return f"set {key}={val}"

def set_env_vars(skip_check=False, **kwargs):
    """
    Add environment variables to the virtual env activation script
    """
    if skip_check:
        with open(activate(), "a") as f:
            for key, val in kwargs.items():
                f.write(f"{env_var(key, val)}\n")
        return
    else:
        with open(activate(), "r+") as f:
            # Get existing file content
            body = f.read()
        with open(activate(), "w") as f:
            # If key is already specified, remove it
            for key, val in kwargs.items():
                pattern = f"{env_var(key, val)}\n"
                body = re.sub(pattern, "", body)
                body += f"{env_var(key, val)}\n"
            f.write(body)
        return

def rm_env_vars(**kwargs):
    # Remove environment variables from the virtual env activation script
    with open(activate(), "r+") as f:
        body = f.read()
        for key, val in kwargs.items():
            pattern = f"{env_var(key, val)}\n"
            body = re.sub(pattern, "", body)
        f.seek(0)
        f.truncate()
        f.write(body)
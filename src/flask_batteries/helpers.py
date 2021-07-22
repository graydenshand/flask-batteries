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


def add_to_config(
    base_config=[],
    production_config=[],
    development_config=[],
    testing_config=[],
):
    """
    Add lines to src/config.py at various marks
    """
    with open(os.path.join("src", "config.py"), "r+") as f:
        lines = f.read().split("\n")

        i = 0
        while i < len(lines):
            if lines[i] == f"{TAB}# --flask_batteries_mark base_config--":
                for item in base_config:
                    lines.insert(i, f"{TAB}{item}")
                    i += 1
            elif lines[i] == f"{TAB}# --flask_batteries_mark production_config--":
                for item in production_config:
                    lines.insert(i, f"{TAB}{item}")
                    i += 1
            elif lines[i] == f"{TAB}# --flask_batteries_mark development_config--":
                for item in development_config:
                    lines.insert(i, f"{TAB}{item}")
                    i += 1
            elif lines[i] == f"{TAB}# --flask_batteries_mark testing_config--":
                for item in testing_config:
                    lines.insert(i, f"{TAB}{item}")
                    i += 1
                break
            i += 1
        f.seek(0)
        f.truncate()
        f.write("\n".join(lines))


def add_to_init(
    imports=[],
    initializations=[],
    attachments=[],
    shell_vars=[],
):
    """
    Add lines to src/__init__.py at various marks
    """
    with open(os.path.join("src", "__init__.py"), "r+") as f:
        lines = f.read().split("\n")

        i = 0
        while i < len(lines):
            if lines[i] == "# --flask_batteries_mark imports--":
                for import_ in imports:
                    lines.insert(i, import_)
                    i += 1
            elif lines[i] == "# --flask_batteries_mark initializations--":
                for init in initializations:
                    lines.insert(i, init)
                    i += 1
            elif lines[i] == f"{TAB}{TAB}# --flask_batteries_mark attachments--":
                for attachment in attachments:
                    lines.insert(i, f"{TAB}{TAB}{attachment}")
                    i += 1
            elif lines[i] == f"{TAB}{TAB}{TAB}# --flask_batteries_mark shell_vars--":
                for shell_var in shell_vars:
                    lines.insert(i, f"{TAB}{TAB}{TAB}{shell_var}")
                    i += 1
                break
            i += 1
        f.seek(0)
        f.truncate()
        f.write("\n".join(lines))


def remove_from_file(filename, lines_to_remove=[]):
    """
    Loop through the lines of a file, removing specified lines
    """
    with open(filename, "r+") as f:
        lines = f.read().split("\n")

        i = 0
        while i < len(lines):
            if lines[i].lstrip(" ") in lines_to_remove:
                del lines[i]
                i -= 1
            i += 1

        f.seek(0)
        f.truncate()
        f.write("\n".join(lines))


def verify_file(filename, lines_to_verify=[]):
    """
    Loop through the lines of a file, verifying specified lines exist
    """
    with open(filename, "r") as f:
        lines = f.read().split("\n")

        i = 0
        counter = 0
        while i < len(lines):
            if lines[i].lstrip(" ") in lines_to_verify:
                counter += 1
            i += 1

        if counter == len(lines_to_verify):
            return True
        else:
            return False


class FlaskBatteriesError(Exception):
    """Base error for package"""


class InstallError(FlaskBatteriesError):
    """Error while installing package"""

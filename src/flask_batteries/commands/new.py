#!/opt/homebrew/bin/python3
import os
import sys
import re
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import subprocess
import click
from pkg_resources import resource_filename
import shutil
import pathspec
import importlib.resources
from ..config import PATH_TO_VENV


@click.command(help="Generate a new Flask-Batteries app")
@click.option('--path-to-venv',default="venv")
def new(path_to_venv):
    if os.name != 'nt':
        name = os.getcwd().split("/")[-1]
    else:
        name = os.getcwd().split("\\")[-1]
    click.echo("Generating new app named: %s" % name)
    env = Environment(
        loader=PackageLoader("flask_batteries", "template"),
        autoescape=select_autoescape(),
    )

    def render_template(filename, **params):
        filename = filename.replace("\\", "/")
        template = env.get_template(filename)
        return template.render(**params)

    def copy_template(filename, **params):
        pattern = r"src[\\/]+assets[\\/]+images"
        match = re.match(pattern, filename)
        if match is None:
            with open(filename, "w+") as f:
                f.write(render_template(filename, **params))
        else:
            # Copy image files directly
            shutil.copyfile(
                resource_filename("flask_batteries", f"template/{filename}"), filename
            )
        return

    def env_var(key, val):
        if os.name != "nt":
            return f"export {key}={val}"
        else:
            return f"set {key}={val}"

    def set_env_vars(skip_check=False, **kwargs):
        # Add environment variable to virtual env activation script
        if os.name != "nt":
            # Posix
            activate = os.path.join(path_to_venv, "bin", "activate")
        else:
            # Windows
            activate = os.path.join(path_to_venv, "Scripts", "activate.bat")
        if skip_check:
            with open(activate, "a") as f:
                for key, val in kwargs.items():
                    f.write(f"{env_var(key, val)}\n")
            return
        else:
            with open(activate, "r") as f:
                # Get existing file content
                body = f.read()
            with open(activate, "w") as f:
                # If key is already specified, remove it
                for key, val in kwargs.items():
                    regex = f"{env_var(key, val)}\n"
                    body = re.sub(regex, "", body) + f"{env_var(key, val)}\n"
                    f.write(body)
            return

    # Look at .gitignore to find files in template not to copy
    print("Opening .gitignore")
    with open(resource_filename("flask_batteries", "template/.gitignore"), "r") as f:
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    ignore_matches = list(
        ignore_spec.match_tree(resource_filename("flask_batteries", "template"))
    )
    # Walk the app template and copy every file and directory
    print("Copying template")
    for dirpath, dirs, files in os.walk(
        resource_filename("flask_batteries", "template")
    ):
        pattern = r"template[\/]*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            if d != "__pycache__":
                resource = os.path.join(path, d).lstrip("\\") if path else d
                print("Creating", resource)
                os.mkdir(resource)
        for f in files:
            resource = os.path.join(path, f).lstrip("\\") if path else f
            print("Copying", resource)
            if resource not in ignore_matches:
                copy_template(resource, name=name)

    # Initialize git repo
    subprocess.run(["git", "init", "--initial-branch=main"])

    # Install PyPI package dependencies
    if os.name != "nt":
        # Posix
        pip = os.path.join(path_to_venv, "bin", "pip")
    else:
        # Windows
        pip = os.path.join(path_to_venv, "Scripts", "pip")
    dependencies = ["flask", "pytest", "requests"]
    subprocess.run(f"{pip} install -q -q " + " ".join(dependencies), shell=True)
    open("requirements.txt", "w+").close()
    subprocess.run(f"{pip} freeze > requirements.txt", shell=True)

    ## Set default environment variables
    envs = {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "SECRET_KEY": os.urandom(24).hex(),
        "PATH_TO_VENV": path_to_venv,
    }
    set_env_vars(skip_check=True, **envs)

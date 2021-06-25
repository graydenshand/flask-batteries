#!/opt/homebrew/bin/python3
import os
import sys
import re
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import subprocess
import click
from pkg_resources import resource_filename


@click.command()
@click.argument("name")
def new(name):
    print("Generating new app named: %s" % name)
    env = Environment(
        loader=PackageLoader("flask_boot", "template"), autoescape=select_autoescape()
    )

    def render_template(filename, **params):
        template = env.get_template(filename)
        return template.render(**params)

    def copy_template(filename, **params):
        with open(filename, "w") as f:
            f.write(render_template(filename, **params))
        return

    def set_env_vars(skip_check=False, **kwargs):
        # Add an environment variable to venv/bin/activate
        if skip_check:
            with open("venv/bin/activate", "a") as f:
                for key, val in kwargs.items():
                    f.write(f"export {key}={val}\n")
            return
        else:
            with open("venv/bin/activate", "r") as f:
                # Get existing file content
                body = f.read()

            with open("venv/bin/activate", "w") as f:
                # If key is already specified, remove it
                for key, val in kwargs.items():
                    regex = f"export {key}={val}\n"
                    body = re.sub(regex, "", body) + f"export {key}={val}\n"
                    f.write(body)
            return

    # Create empty directory and set it as current working directory
    os.mkdir(name)
    os.chdir(name)

    # Walk the app template and copy every file and directory
    for dirpath, dirs, files in os.walk(resource_filename("flask_boot", "template")):
        pattern = r"template\/*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            resource = path + "/" + d if path else d
            if "__pycache__" not in resource:
                os.mkdir(resource)
        for f in files:
            resource = path + "/" + f if path else f
            if "__pycache__" not in resource:
                copy_template(resource, name=name)

    # Initialize git repo
    subprocess.run(["git", "init", "--initial-branch=main"])
    # Initialize virtual env
    subprocess.run(["python3", "-m", "venv", "venv"])
    ## Install requirements
    requirements = ["flask", "pytest"]
    subprocess.run([f"venv/bin/pip", "install"] + requirements)
    ## Set default environment variables
    envs = {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "SECRET_KEY": os.urandom(24).hex(),
    }
    set_env_vars(skip_check=True, **envs)

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
from ..installers import FlaskMigrateInstaller
from ..helpers import set_env_vars, pip

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

@click.command(help="Generate a new Flask-Batteries app")
@click.argument("name", required=False)
@click.option("--path-to-venv", default="venv")
def new(name=None, path_to_venv="venv"):
    click.echo("Generating new app named: %s" % name)

    # Set PATH_TO_VENV env variable, used by FlaskMigrateInstaller later
    os.environ["PATH_TO_VENV"] = path_to_venv

    if name is None:
        # Install in current directory, use directory name as app name
        # assume that virtual environment is already created
        if os.name != "nt":
            name = os.getcwd().split("/")[-1]
        else:
            name = os.getcwd().split("\\")[-1]
    else:
        # Set up project in new directory
        os.mkdir(name)
        os.chdir(name)
        if os.name != 'nt':
            subprocess.run(f"python -m venv {path_to_venv}", shell=True)
        else:
            subprocess.run(f"py -m venv {path_to_venv}", shell=True)

    
    

    # Look at .gitignore to find files in template not to copy
    with open(resource_filename("flask_batteries", "template/.gitignore"), "r") as f:
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    ignore_matches = list(
        ignore_spec.match_tree(resource_filename("flask_batteries", "template"))
    )
    # Walk the app template and copy every file and directory
    for dirpath, dirs, files in os.walk(
        resource_filename("flask_batteries", "template")
    ):
        pattern = r"template[\/]*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            if d != "__pycache__":
                resource = os.path.join(path, d).lstrip("\\") if path else d
                os.mkdir(resource)
        for f in files:
            resource = os.path.join(path, f).lstrip("\\") if path else f
            if resource not in ignore_matches:
                copy_template(resource, name=name)

    # Initialize git repo
    subprocess.run(["git", "init", "--initial-branch=main"])

    # Install PyPI package dependencies
    dependencies = ["flask", "pytest", "requests"]
    if os.environ.get("FLASK_BATTERIES_ENV") not in ("testing", "development"):
        dependencies.append("flask-batteries")
    else:
        assert os.environ.get("FLASK_BATTERIES_PATH") is not None, "FLASK_BATTERIES_PATH env variable not set"
        subprocess.run(f"{pip()} install -q -q -e {os.environ.get('FLASK_BATTERIES_PATH')}", shell=True)
    subprocess.run(f"{pip()} install -q -q " + " ".join(dependencies), shell=True)
    open("requirements.txt", "w+").close()
    subprocess.run(f"{pip()} freeze > requirements.txt", shell=True)

    ## Set default environment variables
    envs = {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "SECRET_KEY": os.urandom(24).hex(),
        "PATH_TO_VENV": path_to_venv,
    }
    set_env_vars(skip_check=True, **envs)

    # Install Flask-Migrate and Flask-SQLAlchemy
    FlaskMigrateInstaller.install()

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
from ..config import PATH_TO_VENV, TAB
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

def copy_template(filename, target=None, **params):
    if target is None:
        target = filename
    pattern = r"src[\\/]+assets[\\/]+static"
    match = re.match(pattern, filename)
    if match is None:
        with open(target, "w+") as f:
            f.write(render_template(filename, **params))
    else:
        # Copy image files directly
        shutil.copyfile(
            resource_filename("flask_batteries", f"template/{filename}"), target
        )
    return

@click.command(help="Generate a new Flask-Batteries app")
@click.argument("name", required=False)
@click.option("--path-to-venv", default="venv", help="Path to virtual environment directory")
@click.option("--skip-webpack", is_flag=True, help="Use static folder instead of Webpack asset pipeline")
def new(name, path_to_venv, skip_webpack):
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
        try:
            os.mkdir(name)
        except FileExistsError:
            raise click.ClickException(f"Can't create directory '{name}' as it already exists")
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
                copy_template(resource, name=name, skip_webpack=skip_webpack)

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


    # Remove webpack files if necessary
    if skip_webpack:
        shutil.rmtree(os.path.join("src", "assets"))
        os.remove("webpack.config.js")
        os.mkdir(os.path.join("src", "static"))
        os.mkdir(os.path.join("src", "static", "stylesheets"))
        os.mkdir(os.path.join("src", "static", "images"))
        os.mkdir(os.path.join("src", "static", "javascript"))


        copy_template(os.path.join("src", "assets", "static", "images", "flask-logo.png"), target=os.path.join("src", "static", "images", "flask-logo.png"))
        copy_template(os.path.join("src", "assets", "static", "images", "flask-icon.png"), target=os.path.join("src", "static", "images", "flask-icon.png"))
        copy_template(os.path.join("src", "assets", "stylesheets", "base.scss"), target=os.path.join("src", "static", "stylesheets", "base.css"))

        with open(os.path.join("src", "config.py"), 'r+') as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == f"{TAB}# --flask_batteries_mark base_config--":
                    lines.insert(i, f"{TAB}FLASK_BATTERIES_USE_WEBPACK=False")
                    break
                i += 1

            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))


    # Install Flask-Migrate and Flask-SQLAlchemy
    FlaskMigrateInstaller.install()

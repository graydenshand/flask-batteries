#!/opt/homebrew/bin/python3
import os
import sys
import re
from datetime import datetime
import subprocess
import click
from pkg_resources import resource_filename, get_distribution
import shutil
import pathspec
import importlib.resources
from ..config import PATH_TO_VENV, TAB
from ..installers import (
    InstallManager,
    FlaskMigrateInstaller,
    FlaskSQLAlchemyInstaller,
    FlaskMarshmallowInstaller,
)
from ..helpers import (
    set_env_vars,
    pip,
    add_to_config,
    copy_template,
    FlaskBatteriesError,
)


@click.command(help="Generate a new Flask-Batteries app")
@click.argument("name", required=False)
@click.option(
    "--path-to-venv", default="venv", help="Path to virtual environment directory"
)
@click.option(
    "--skip-webpack",
    is_flag=True,
    help="Use static folder instead of Webpack asset pipeline",
)
@click.option(
    "--git-initial-branch",
    help="The name of the main git branch for the project. Defaults to 'main'.",
    default="main",
)
@click.option(
    "--skip-db",
    is_flag=True,
    help="Don't install Flask-SQLAlchemy & Flask-Migrate",
)
def new(name, path_to_venv, skip_webpack, git_initial_branch, skip_db):

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
            raise click.ClickException(
                f"Can't create directory '{name}' as it already exists"
            )
        os.chdir(name)

    click.echo("Generating new app named: %s" % name)

    if not os.path.exists(path_to_venv):
        if os.name != "nt":
            subprocess.run(["python3", "-m", "venv", path_to_venv], check=True)
        else:
            subprocess.run(["py", "-m", "venv", path_to_venv], check=True)

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
    subprocess.run(
        [f"git init --initial-branch={git_initial_branch}"],
        check=True,
        shell=True,
        stdout=subprocess.DEVNULL,
    )

    # Install PyPI package dependencies
    dependencies = ["flask", "pytest", "requests"]
    if os.environ.get("FLASK_BATTERIES_ENV") not in ("testing", "development"):
        # Install
        current_version = get_distribution("flask-batteries").version
        dependencies.append("flask-batteries==" + current_version)
    else:
        assert (
            os.environ.get("FLASK_BATTERIES_PATH") is not None
        ), "FLASK_BATTERIES_PATH env variable not set"
        subprocess.run(
            [
                pip(),
                "install",
                "-q",
                "-q",
                "-e",
                os.environ.get("FLASK_BATTERIES_PATH"),
            ],
            check=True,
        )

    subprocess.run(
        [pip(), "install", "-q", "-q"] + dependencies,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    open("requirements.txt", "w+").close()
    reqs_result = subprocess.run(
        [f"{pip()} freeze -q -q > requirements.txt"],
        stdout=subprocess.DEVNULL,
        shell=True,
        check=True,
    )

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

        copy_template(
            os.path.join("src", "assets", "static", "images", "flask-logo.png"),
            target=os.path.join("src", "static", "images", "flask-logo.png"),
        )
        copy_template(
            os.path.join("src", "assets", "static", "images", "flask-icon.png"),
            target=os.path.join("src", "static", "images", "flask-icon.png"),
        )
        copy_template(
            os.path.join("src", "assets", "stylesheets", "_base.scss"),
            target=os.path.join("src", "static", "stylesheets", "base.css"),
        )

        add_to_config(development_config=["BATTERIES_USE_WEBPACK = False"])

    # Install Flask-SQLAlchemy, Flask-Migrate, and Flask-Marshmallow
    if not skip_db:
        InstallManager.install(FlaskSQLAlchemyInstaller)
        InstallManager.install(FlaskMigrateInstaller)
        InstallManager.install(FlaskMarshmallowInstaller)

    click.echo("Done")

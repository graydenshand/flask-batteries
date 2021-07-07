from .base_installer import FlaskExtInstaller
import click
import os
import subprocess
import shutil

PATH_TO_VENV = os.environ.get("FLASK_BOOT_PATH_TO_VENV", "venv")


class FlaskSQLAlchemyInstaller(FlaskExtInstaller):
    @staticmethod
    def install():
        # Install package from PyPI
        subprocess.run(
            f"{PATH_TO_VENV}/bin/pip install -q -q flask-sqlalchemy", shell=True
        )
        click.secho("Installed PyPI package `flask-sqlalchemy`", fg="green")
        subprocess.run(
            f"{PATH_TO_VENV}/bin/pip freeze -q -q > requirements.txt", shell=True
        )
        click.secho("Updated requriements.txt", fg="green")

        # Edit __init__.py
        with open("src/__init__.py", "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                print(lines[i])
                if lines[i] == "# --flask_batteries_mark import_packages--":
                    lines.insert(i, "from flask_sqlalchemy import SQLAlchemy")
                    i += 1  # add an extra one to i
                elif lines[i] == "# --flask_batteries_mark init_extensions--":
                    lines.insert(i, "db = SQLAlchemy()")
                    i += 1  # add an extra one to i
                elif lines[i] == "\t\t# --flask_batteries_mark attach_extensions--":
                    lines.insert(i, "\t\tdb.init_app(app)")
                    lines.insert(i + 1, "\t\tdb.create_all()")
                    break
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho("Updated src/__init__.py", fg="green")

        # Create a 'models' folder if one does not exist
        if not os.path.exists("src/models"):
            os.mkdir("src/models")
            click.secho("Created src/models/", fg="green")
            open("src/models/__init__.py", "w+").close()
            click.secho("Created src/models/__init__.py", fg="green")

        # Edit config.py
        with open("src/config.py", "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark base_config--":
                    lines.insert(
                        i, '\tSQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")'
                    )
                    lines.insert(i + 1, "\tSQLALCHEMY_TRACK_MODIFICATIONS = False")
                    break
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho("Updated src/config.py", fg="green")

    @staticmethod
    def uninstall():
        # Remove initialization from __init__.py and create_app() func
        with open("src/__init__.py", "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "from flask_sqlalchemy import SQLAlchemy":
                    del lines[i]
                    i -= 1  # keep cursor in same position
                elif lines[i] == "db = SQLAlchemy()":
                    del lines[i]
                    i -= 1  # keep cursor in same position
                elif (
                    lines[i] == "\t\tdb.init_app(app)"
                    or lines[i] == "\t\tdb.create_all()"
                ):
                    del lines[i]
                    i -= 1  # keep cursor in same position
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho("Updated src/__init__.py", fg="red")
        # Delete models folder
        if os.path.exists("src/models"):
            shutil.rmtree("src/models")
            click.secho("Destroyed src/models/", fg="red")

        # Edit config.py
        with open("src/config.py", "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if "SQLALCHEMY_" in lines[i]:
                    del lines[i]
                    i -= 1
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho("Updated src/config.py", fg="red")

        # Uninstall package from PyPI
        subprocess.run(
            f"{PATH_TO_VENV}/bin/pip install -q -q flask-sqlalchemy", shell=True
        )
        click.secho("Uninstalled PyPI package `flask-sqlalchemy`", fg="red")
        subprocess.run(
            f"{PATH_TO_VENV}/bin/pip freeze -q -q > requirements.txt", shell=True
        )
        click.secho("Updated requirements.txt", fg="red")

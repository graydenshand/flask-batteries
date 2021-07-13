from .base_installer import FlaskExtInstaller
import click
import os
import subprocess
import shutil
from ..config import PATH_TO_VENV, TAB

if os.name != "nt":
    # Posix
    pip = os.path.join(PATH_TO_VENV, "bin", "pip")
else:
    # Windows
    pip = os.path.join(PATH_TO_VENV, "Scripts", "pip")


class FlaskSQLAlchemyInstaller(FlaskExtInstaller):
    @staticmethod
    def install():
        # Install package from PyPI

        subprocess.run(f"{pip} install -q -q flask-sqlalchemy", shell=True)
        click.secho("Installed PyPI package `flask-sqlalchemy`", fg="green")
        subprocess.run(f"{pip} freeze -q -q > requirements.txt", shell=True)
        click.secho("Updated requirements.txt", fg="green")

        # Edit __init__.py
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark import_packages--":
                    lines.insert(i, "from flask_sqlalchemy import SQLAlchemy")
                    i += 1  # add an extra one to i
                elif lines[i] == "# --flask_batteries_mark init_extensions--":
                    lines.insert(i, "db = SQLAlchemy()")
                    i += 1  # add an extra one to i
                elif (
                    lines[i]
                    == f"{TAB}{TAB}# --flask_batteries_mark attach_extensions--"
                ):
                    lines.insert(i, f"{TAB}{TAB}db.init_app(app)")
                    lines.insert(i + 1, f"{TAB}{TAB}db.create_all()")
                    break
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', '__init__.py')}", fg="green")

        # Create a 'models' folder if one does not exist
        if not os.path.exists(os.path.join("src", "models")):
            os.mkdir(os.path.join("src", "models"))
            click.secho(f"Created {os.path.join('src', 'models')}", fg="green")
            open(os.path.join("src", "models", "__init__.py"), "w+").close()
            click.secho(
                f"Created {os.path.join('src', 'models', '__init__.py')}", fg="green"
            )

        # Edit config.py
        with open(os.path.join("src", "config.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark base_config--":
                    lines.insert(
                        i,
                        f'{TAB}SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")',
                    )
                    lines.insert(i + 1, f"{TAB}SQLALCHEMY_TRACK_MODIFICATIONS = False")
                    break
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', 'config.py')}", fg="green")

    @staticmethod
    def uninstall():
        # Remove initialization from __init__.py and create_app() func
        with open(os.path.join("src", "__init__.py"), "r+") as f:
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
                    lines[i] == f"{TAB}{TAB}db.init_app(app)"
                    or lines[i] == f"{TAB}{TAB}db.create_all()"
                ):
                    del lines[i]
                    i -= 1  # keep cursor in same position
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', '__init__.py')}", fg="red")
        # Delete models folder
        if os.path.exists(os.path.join("src", "models")):
            shutil.rmtree(os.path.join("src", "models"))
            click.secho(f"Destroyed {os.path.join('src', 'models')}", fg="red")

        # Edit config.py
        with open(os.path.join("src", "config.py"), "r+") as f:
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
        click.secho(f"Updated {os.path.join('src', 'config.py')}", fg="red")

        # Uninstall package from PyPI
        subprocess.run(f"{pip} install -q -q flask-sqlalchemy", shell=True)
        click.secho("Uninstalled PyPI package `flask-sqlalchemy`", fg="red")
        subprocess.run(f"{pip} freeze -q -q > requirements.txt", shell=True)
        click.secho("Updated requirements.txt", fg="red")

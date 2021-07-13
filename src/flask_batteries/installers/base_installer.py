import click
import os
import subprocess
from ..config import PATH_TO_VENV, TAB

if os.name != "nt":
    # Posix
    pip = os.path.join(PATH_TO_VENV, "bin", "pip")
else:
    # Windows
    pip = os.path.join(PATH_TO_VENV, "Scripts", "pip")

class FlaskExtInstaller:
    package_name = None
    imports = []
    inits = []
    attachments = []
    base_config = []
    production_config = []
    development_config = []
    testing_config = []

    @classmethod
    def install(cls):
        if cls.package_name is None:
            raise NotImplementedError()
        # Install package from PyPI
        subprocess.run(f"{pip} install -q -q {cls.package_name}", shell=True)
        click.secho(f"Installed PyPI package `{cls.package_name}`", fg="green")
        subprocess.run(f"{pip} freeze -q -q > requirements.txt", shell=True)
        click.secho("Updated requirements.txt", fg="green")

        # Edit __init__.py
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark import_packages--":
                    for import_ in cls.imports:
                        lines.insert(i, import_)
                        i += 1
                elif lines[i] == "# --flask_batteries_mark init_extensions--":
                    for init in cls.inits:
                        lines.insert(i, init)
                        i += 1
                elif (
                    lines[i]
                    == f"{TAB}{TAB}# --flask_batteries_mark attach_extensions--"
                ):
                    for attachment in cls.attachments:
                        lines.insert(i, f"{TAB}{TAB}{attachment}")
                        i+=1
                    break
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', '__init__.py')}", fg="green")

        # Edit config.py
        with open(os.path.join("src", "config.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark base_config--":
                    for item in cls.base_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == "# --flask_batteries_mark production_config--":
                    for item in cls.production_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == "# --flask_batteries_mark development_config--":
                    for item in cls.development_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == "# --flask_batteries_mark testing_config--":
                    for item in cls.testing_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', 'config.py')}", fg="green")

    @classmethod
    def uninstall(cls):
        if cls.package_name is None:
            raise NotImplementedError()

        # Uninstall package from PyPI
        subprocess.run(f"{pip} uninstall -q -q {cls.package_name}", shell=True)
        click.secho(f"Uninstalled PyPI package `{cls.package_name}`", fg="red")
        subprocess.run(f"{pip} freeze -q -q > requirements.txt", shell=True)
        click.secho("Updated requirements.txt", fg="red")

        # Remove initialization from __init__.py and create_app() func
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark attach_extensions--":
                    break
                elif (
                        lines[i].lstrip(" ") in cls.imports
                        or lines[i].lstrip(" ") in cls.inits
                        or lines[i].lstrip(" ") in cls.attachments
                    ):
                        del lines[i]
                        i -= 1
                i += 1
                
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', '__init__.py')}", fg="red")

        # Edit config.py
        with open(os.path.join("src", "config.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark testing_config--":
                    break
                elif (
                    lines[i].lstrip(" ") in cls.base_config
                    or lines[i].lstrip(" ") in cls.production_config
                    or lines[i].lstrip(" ") in cls.development_config
                    or lines[i].lstrip(" ") in cls.testing_config
                ):
                    del lines[i]
                    i -= 1
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', 'config.py')}", fg="red")

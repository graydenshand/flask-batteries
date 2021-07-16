import click
import os
import subprocess
import re
import sys
from ..config import PATH_TO_VENV, TAB
from ..helpers import pip, activate, env_var, rm_env_vars, set_env_vars


class FlaskExtInstaller:
    package_name = None
    imports = []
    inits = []
    attachments = []
    base_config = []
    production_config = []
    development_config = []
    testing_config = []
    dependencies = []
    pypi_dependencies = []
    envs = {}

    @classmethod
    def install(cls):
        if cls.package_name is None:
            raise NotImplementedError()

        # Prevent installing same package twice
        if cls.verify():
            click.secho(f"{cls.package_name} is already installed")
            return

        # Install any dependencies if not already installed
        for dep in cls.dependencies:
            dep.install()

        # Install package from PyPI
        subprocess.run(
            f"{pip()} install -q -q {cls.package_name} {' '.join(cls.pypi_dependencies)}",
            shell=True,
        )
        click.secho(f"Installed PyPI package `{cls.package_name}`", fg="green")
        subprocess.run(f"{pip()} freeze -q -q > requirements.txt", shell=True)
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
                        i += 1
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
                if lines[i] == f"{TAB}# --flask_batteries_mark base_config--":
                    for item in cls.base_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == f"{TAB}# --flask_batteries_mark production_config--":
                    for item in cls.production_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == f"{TAB}# --flask_batteries_mark development_config--":
                    for item in cls.development_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                elif lines[i] == f"{TAB}# --flask_batteries_mark testing_config--":
                    for item in cls.testing_config:
                        lines.insert(i, f"{TAB}{item}")
                        i += 1
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines))
        click.secho(f"Updated {os.path.join('src', 'config.py')}", fg="green")

        # Add envs
        set_env_vars(**cls.envs)

    @classmethod
    def uninstall(cls):
        if cls.package_name is None:
            raise NotImplementedError()

        # Uninstall package from PyPI
        subprocess.run(
            f"{pip()} uninstall -q -q -y {cls.package_name} {' '.join(cls.pypi_dependencies)}",
            shell=True,
        )
        click.secho(f"Uninstalled PyPI package `{cls.package_name}`", fg="red")
        subprocess.run(f"{pip()} freeze -q -q > requirements.txt", shell=True)
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

        # Remove env vars
        rm_env_vars(**cls.envs)

    @classmethod
    def verify(cls, verbose=False):
        if cls.package_name is None:
            raise NotImplementedError()

        for dep in cls.dependencies:
            if not dep.verify():
                if verbose:
                    click.secho(
                        f"Package Verification Error: {cls.package_name} is missing depencency -- {dep}"
                    )
                return False

        # Verify package is istalled from PyPI
        reqs = subprocess.check_output(f"{pip()} freeze -q -q", shell=True)
        installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
        if cls.package_name not in installed_packages:
            if verbose:
                click.secho(
                    f"Package Verification Error: {cls.package_name} not found in package manager",
                    fg="red",
                )
            return False
        if verbose:
            click.secho("Verified PyPI installation", fg="green")

        # Remove initialization from __init__.py and create_app() func
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            counter = 0
            while i < len(lines):
                if lines[i] == "# --flask_batteries_mark attach_extensions--":
                    break
                elif (
                    lines[i].lstrip(" ") in cls.imports
                    or lines[i].lstrip(" ") in cls.inits
                    or lines[i].lstrip(" ") in cls.attachments
                ):
                    counter += 1
                i += 1
            if counter != len(cls.imports) + len(cls.inits) + len(cls.attachments):
                if verbose:
                    click.secho(
                        f"Package Verification Error: {cls.package_name} __init__.py missing expected lines",
                        fg="red",
                    )
                return False
        if verbose:
            click.secho(f"Verified {os.path.join('src', '__init__.py')}", fg="green")

        # Edit config.py
        with open(os.path.join("src", "config.py"), "r+") as f:
            lines = f.read().split("\n")

            i = 0
            counter = 0
            while i < len(lines):
                if lines[i] == f"{TAB}# --flask_batteries_mark testing_config--":
                    break
                elif (
                    lines[i].lstrip(" ") in cls.base_config
                    or lines[i].lstrip(" ") in cls.production_config
                    or lines[i].lstrip(" ") in cls.development_config
                    or lines[i].lstrip(" ") in cls.testing_config
                ):
                    counter += 1
                i += 1
            if counter != len(cls.base_config) + len(cls.production_config) + len(
                cls.development_config
            ) + len(cls.testing_config):
                if verbose:
                    click.secho(
                        f"Package Verification Error: {cls.package_name} config.py missing expected lines",
                        fg="red",
                    )
                return False
            if verbose:
                click.secho(f"Verified {os.path.join('src', 'config.py')}", fg="green")

        # Verify ENVS
        with open(activate(), "r") as f:
            body = f.read()
            for k, v in cls.envs.items():
                if f"{env_var(k,v)}\n" not in body:
                    if verbose:
                        click.secho(
                            f"Package Verification Error: {cls.package_name} env variables missing from {activate}"
                        )
                    return False
        return True

    

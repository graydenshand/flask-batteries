import click
import os
import subprocess
import re
import sys
from ..config import PATH_TO_VENV, TAB
from ..helpers import *


class FlaskExtInstaller:
    package_name = None
    imports = []
    inits = []
    attachments = []
    shell_vars = []
    base_config = []
    production_config = []
    development_config = []
    testing_config = []
    pypi_dependencies = []
    envs = {}

    @classmethod
    def install(cls):
        # Prevent installing same package twice
        if cls.verify():
            raise InstallError(f"{cls.package_name} is already installed")

        # Install package from PyPI
        if cls.package_name is not None:
            subprocess.run(
                [pip(), "install", "-q", "-q", cls.package_name]
                + cls.pypi_dependencies,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                f"{pip()} freeze -q -q > requirements.txt",
                stdout=subprocess.DEVNULL,
                shell=True,
            )

        # Edit __init__.py
        add_to_init(
            imports=cls.imports,
            initializations=cls.inits,
            attachments=cls.attachments,
            shell_vars=cls.shell_vars,
        )

        # Edit config.py
        add_to_config(
            base_config=cls.base_config,
            production_config=cls.production_config,
            development_config=cls.development_config,
            testing_config=cls.testing_config,
        )

        # Add envs
        set_env_vars(**cls.envs)

    @classmethod
    def uninstall(cls):
        if cls.package_name is not None:
            # Uninstall package from PyPI
            subprocess.run(
                [pip(), "uninstall", "-q", "-q", "-y", cls.package_name]
                + cls.pypi_dependencies,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                f"{pip()} freeze -q -q > requirements.txt",
                stdout=subprocess.DEVNULL,
                shell=True,
            )

        # Remove initialization from __init__.py and create_app() func
        lines_to_remove = cls.imports + cls.inits + cls.attachments + cls.shell_vars
        remove_from_file(os.path.join("src", "__init__.py"), lines_to_remove)

        # Edit config.py
        lines_to_remove = (
            cls.base_config
            + cls.production_config
            + cls.development_config
            + cls.testing_config
        )
        remove_from_file(os.path.join("src", "config.py"), lines_to_remove)

        # Remove env vars
        rm_env_vars(**cls.envs)

    @classmethod
    def verify(cls, raise_for_error=False):
        # Verify package is istalled from PyPI
        if cls.package_name is not None:
            reqs = subprocess.check_output(f"{pip()} freeze -q -q", shell=True)
            installed_packages = [r.decode().split("==")[0] for r in reqs.split()]
            if cls.package_name not in installed_packages:
                if raise_for_error:
                    raise InstallError(f"{cls.package_name} not installed from PyPI")
                return False
        # Verify __init__.py
        lines_to_verify = cls.imports + cls.inits + cls.attachments + cls.shell_vars
        if not verify_file(os.path.join("src", "__init__.py"), lines_to_verify):
            if raise_for_error:
                raise InstallError(f"{cls} __init__.py is incorrect")
            return False

        # Verify config.py
        lines_to_verify = (
            cls.base_config
            + cls.production_config
            + cls.development_config
            + cls.testing_config
        )
        if not verify_file(os.path.join("src", "config.py"), lines_to_verify):
            if raise_for_error:
                raise InstallError(f"{cls} config.py is incorrect")
            return False

        # Verify ENVS
        with open(activate(), "r") as f:
            body = f.read()
            for k, v in cls.envs.items():
                pattern = rf"(use|export) {k}=(.*)\n"
                if re.search(pattern, body) is None:
                    if raise_for_error:
                        raise InstallError(f"{cls} ENVs missing from venv activate")
                    return False
        return True

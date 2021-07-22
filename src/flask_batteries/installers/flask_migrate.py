from .base_installer import FlaskExtInstaller
from .flask_sqlalchemy import FlaskSQLAlchemyInstaller
import subprocess
import shutil
import click
import os
from ..helpers import activate
import sys


class FlaskMigrateInstaller(FlaskExtInstaller):
    package_name = "Flask-Migrate"
    dependencies = [FlaskSQLAlchemyInstaller]
    imports = ["from flask_migrate import Migrate"]
    inits = ['migrate = Migrate(db, directory="src/migrations")']
    attachments = ["migrate.init_app(app)"]

    @classmethod
    def install(cls):
        super().install()
        path_to_venv = os.environ.get("PATH_TO_VENV", "venv")
        if os.name != "nt":
            result = subprocess.run(
                f"source {activate()} && flask db init",
                shell=True,
                stdout=subprocess.DEVNULL,
            )
        else:
            result = subprocess.run(
                f"{path_to_venv}\\Scripts\\activate && flask db init",
                shell=True,
                stdout=subprocess.DEVNULL,
            )
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            raise Exception("Unable to initalize Flask-Migrate")

    @classmethod
    def uninstall(cls):
        super().uninstall()
        if os.path.exists(os.path.join("src", "migrations")):
            shutil.rmtree(os.path.join("src", "migrations"))

    @classmethod
    def verify(cls):
        if not os.path.exists(os.path.join("src", "migrations")):
            return False
        else:
            return super().verify()

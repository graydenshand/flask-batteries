from .base_installer import FlaskExtInstaller
import click
import os
import shutil
from sqlalchemy_utils import create_database, database_exists


class FlaskWTFInstaller(FlaskExtInstaller):
    package_name = "Flask-WTF"

    @classmethod
    def install(cls):
        super().install()
        # Create a 'forms' folder if one does not exist
        if not os.path.exists(os.path.join("src", "forms")):
            os.mkdir(os.path.join("src", "forms"))
            open(os.path.join("src", "forms", "__init__.py"), "w+").close()

        if not os.path.exists(os.path.join("test", "forms")):
            os.mkdir(os.path.join("test", "forms"))
            open(os.path.join("test", "forms", "__init__.py"), "w+").close()

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete forms folder
        if os.path.exists(os.path.join("src", "forms")):
            shutil.rmtree(os.path.join("src", "forms"))

        if os.path.exists(os.path.join("test", "forms")):
            shutil.rmtree(os.path.join("test", "forms"))

    @classmethod
    def verify(cls, verbose=False):
        if (
            not os.path.exists(os.path.join("src", "forms"))
            or not os.path.exists(os.path.join("src", "forms", "__init__.py"))
            or not os.path.exists(os.path.join("test", "forms"))
            or not os.path.exists(os.path.join("test", "forms", "__init__.py"))
        ):
            return False
        else:
            return super().verify()

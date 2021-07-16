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
            click.secho(f"Created {os.path.join('src', 'forms')}", fg="green")
            open(os.path.join("src", "forms", "__init__.py"), "w+").close()
            click.secho(
                f"Created {os.path.join('src', 'forms', '__init__.py')}", fg="green"
            )

        if not os.path.exists(os.path.join("test", "forms")):
            os.mkdir(os.path.join("test", "forms"))
            click.secho(f"Created {os.path.join('test', 'forms')}", fg="green")
            open(os.path.join("test", "forms", "__init__.py"), "w+").close()
            click.secho(
                f"Created {os.path.join('test', 'forms', '__init__.py')}", fg="green"
            )

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete forms folder
        if os.path.exists(os.path.join("src", "forms")):
            shutil.rmtree(os.path.join("src", "forms"))
            click.secho(f"Destroyed {os.path.join('src', 'forms')}", fg="red")

        if os.path.exists(os.path.join("test", "forms")):
            shutil.rmtree(os.path.join("test", "forms"))
            click.secho(f"Destroyed {os.path.join('test', 'forms')}", fg="red")

    @classmethod
    def verify(cls, verbose=False):
        if (
            not os.path.exists(os.path.join("src", "forms"))
            or not os.path.exists(os.path.join("src", "forms", "__init__.py"))
            or not os.path.exists(os.path.join("test", "forms"))
            or not os.path.exists(os.path.join("test", "forms", "__init__.py"))
        ):
            if verbose:
                click.secho(
                    f"Package Verification Error: Flask-WTF `forms` directory not found",
                    fg="red",
                )
            return False
        else:
            return super().verify()

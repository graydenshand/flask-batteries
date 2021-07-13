from .base_installer import FlaskExtInstaller
import click
import os
import shutil

class FlaskSQLAlchemyInstaller(FlaskExtInstaller):
    package_name = "flask-sqlalchemy"
    imports = ["from flask_sqlalchemy import SQLAlchemy"]
    inits = ["db = SQLAlchemy()"]
    attachments = ["db.init_app(app)", "db.create_all()"]
    base_config = ["SQLALCHEMY_DATABASE_URI=os.environ.get(\"DATABASE_URL\")", "SQLALCHEMY_TRACK_MODIFICATIONS = False"]

    @classmethod
    def install(cls):
        super().install()
        # Create a 'models' folder if one does not exist
        if not os.path.exists(os.path.join("src", "models")):
            os.mkdir(os.path.join("src", "models"))
            click.secho(f"Created {os.path.join('src', 'models')}", fg="green")
            open(os.path.join("src", "models", "__init__.py"), "w+").close()
            click.secho(
                f"Created {os.path.join('src', 'models', '__init__.py')}", fg="green"
            )

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete models folder
        if os.path.exists(os.path.join("src", "models")):
            shutil.rmtree(os.path.join("src", "models"))
            click.secho(f"Destroyed {os.path.join('src', 'models')}", fg="red")

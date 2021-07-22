from .base_installer import FlaskExtInstaller
import click
import os
import shutil
from sqlalchemy_utils import create_database, database_exists


class FlaskSQLAlchemyInstaller(FlaskExtInstaller):
    package_name = "Flask-SQLAlchemy"
    pypi_dependencies = ["psycopg2", "sqlalchemy-utils"]
    imports = ["from flask_sqlalchemy import SQLAlchemy"]
    inits = ["db = SQLAlchemy()"]
    attachments = ["db.init_app(app)", "db.create_all()"]
    base_config = [
        'SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")',
        "SQLALCHEMY_TRACK_MODIFICATIONS = False",
    ]
    envs = {}

    @classmethod
    def install(cls):
        if os.name != "nt":
            name = os.getcwd().split("/")[-1]
        else:
            name = os.getcwd().split("\\")[-1]
        cls.envs["DATABASE_URL"] = f"postgresql://localhost:5432/{name}"
        super().install()
        # Create a 'models' folder if one does not exist
        if not os.path.exists(os.path.join("src", "models")):
            os.mkdir(os.path.join("src", "models"))
            open(os.path.join("src", "models", "__init__.py"), "w+").close()
        if not os.path.exists(os.path.join("test", "models")):
            os.mkdir(os.path.join("test", "models"))
            open(os.path.join("test", "models", "__init__.py"), "w+").close()

        # Set up a database if needed
        if not database_exists(cls.envs["DATABASE_URL"]):
            create_database(cls.envs["DATABASE_URL"])

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete models folder
        if os.path.exists(os.path.join("src", "models")):
            shutil.rmtree(os.path.join("src", "models"))

        if os.path.exists(os.path.join("test", "models")):
            shutil.rmtree(os.path.join("test", "models"))

    @classmethod
    def verify(cls):
        if (
            not os.path.exists(os.path.join("src", "models"))
            or not os.path.exists(os.path.join("src", "models", "__init__.py"))
            or not os.path.exists(os.path.join("test", "models"))
            or not os.path.exists(os.path.join("test", "models", "__init__.py"))
        ):
            return False
        else:
            return super().verify()

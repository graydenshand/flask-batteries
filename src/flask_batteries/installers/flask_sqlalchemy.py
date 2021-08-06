from .base_installer import FlaskExtInstaller
import click
import os
import shutil
from sqlalchemy_utils import create_database, database_exists
from ..helpers import InstallError, TAB
import re


class FlaskSQLAlchemyInstaller(FlaskExtInstaller):
    package_name = "Flask-SQLAlchemy"
    pypi_dependencies = ["psycopg2"]
    imports = ["from flask_sqlalchemy import SQLAlchemy"]
    inits = ["db = SQLAlchemy()"]
    attachments = ["db.init_app(app)", "db.create_all()"]
    shell_vars = ['"db": db,']
    base_config = [
        'SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")',
        "SQLALCHEMY_TRACK_MODIFICATIONS = False",
    ]
    development_config = [
        'SQLALCHEMY_DATABASE_URI=os.environ.get("DEV_DATABASE_URL")',
    ]
    testing_config = [
        'SQLALCHEMY_DATABASE_URI=os.environ.get("TEST_DATABASE_URL")',
    ]
    envs = {}

    @classmethod
    def install(cls):
        if os.name != "nt":
            name = os.getcwd().split("/")[-1]
        else:
            name = os.getcwd().split("\\")[-1]
        cls.envs["DEV_DATABASE_URL"] = f"postgresql://localhost:5432/{name}_development"
        cls.envs["TEST_DATABASE_URL"] = f"postgresql://localhost:5432/{name}_test"
        super().install()
        # Create a 'models' folder if one does not exist
        if not os.path.exists(os.path.join("src", "models")):
            os.mkdir(os.path.join("src", "models"))
            open(os.path.join("src", "models", "__init__.py"), "w+").close()
        if not os.path.exists(os.path.join("test", "models")):
            os.mkdir(os.path.join("test", "models"))
            open(os.path.join("test", "models", "__init__.py"), "w+").close()

        # Set up a database if needed
        if not database_exists(cls.envs["DEV_DATABASE_URL"]):
            create_database(cls.envs["DEV_DATABASE_URL"])
        if not database_exists(cls.envs["TEST_DATABASE_URL"]):
            create_database(cls.envs["TEST_DATABASE_URL"])

        # Add db setup to main test fixture
        with open(os.path.join("test", "fixtures.py"), "r+") as f:
            content = f.read().split("\n")
            i = 0
            while i < len(content):
                line = content[i]
                pattern = "from src import create_app"
                if re.match(pattern, line):
                    content[i] = line + ", db"

                pattern = "yield app"
                if re.search(pattern, line):
                    content.insert(i + 1, f"{TAB}{TAB}db.session.close()")
                    content.insert(i + 2, f"{TAB}{TAB}db.drop_all()")
                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(content))

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete models folder
        if os.path.exists(os.path.join("src", "models")):
            shutil.rmtree(os.path.join("src", "models"))

        if os.path.exists(os.path.join("test", "models")):
            shutil.rmtree(os.path.join("test", "models"))

        # Add db setup to main test fixture
        with open(os.path.join("test", "fixtures.py"), "r+") as f:
            content = f.read().split("\n")
            i = 0
            while i < len(content):
                line = content[i]
                pattern = "from src import.*?, db"
                if re.match(pattern, line):
                    content[i] = line.replace(", db", "")

                pattern = "db.session.close()"
                if re.search(pattern, line):
                    del content[i]
                    i -= 1

                pattern = "db.drop_all()"
                if re.search(pattern, line):
                    del content[i]

                i += 1
            f.seek(0)
            f.truncate()
            f.write("\n".join(content))

    @classmethod
    def verify(cls, raise_for_error=False):
        if (
            not os.path.exists(os.path.join("src", "models"))
            or not os.path.exists(os.path.join("src", "models", "__init__.py"))
            or not os.path.exists(os.path.join("test", "models"))
            or not os.path.exists(os.path.join("test", "models", "__init__.py"))
        ):
            if raise_for_error:
                raise InstallError(f"{cls} models directory does not exist")
            return False

        with open(os.path.join("test", "fixtures.py"), "r") as f:
            content = f.read()
            pattern = "from src import.*?, db"
            if not re.search(pattern, content):
                if raise_for_error:
                    raise InstallError(f"{cls} test fixture not configured correctly")
                return False

                pattern = "db.session.close()"
                if not re.search(pattern, content):
                    if raise_for_error:
                        raise InstallError(
                            f"{cls} test fixture not configured correctly"
                        )
                    return False

                pattern = "db.drop_all()"
                if not re.search(pattern, content):
                    if raise_for_error:
                        raise InstallError(
                            f"{cls} test fixture not configured correctly"
                        )
                    return False
                i += 1

        return super().verify(raise_for_error=raise_for_error)

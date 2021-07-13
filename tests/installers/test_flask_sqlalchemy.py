from ..conf_tests import app, cli
from flask_batteries import install
from flask_batteries.installers import FlaskSQLAlchemyInstaller
import os
from flask_batteries.config import TAB


def test_flask_sqlalchemy_installer(app, cli):
    # Install the extension
    FlaskSQLAlchemyInstaller.install()

    # Check that models directory exists
    assert os.path.exists(os.path.join("src", "models"))
    assert os.path.exists(os.path.join("src", "models", "__init__.py"))

    # Check that __init__.py contains needed lines
    with open(os.path.join("src", "__init__.py"), "r") as f:
        content = f.read().split("\n")

    assert "from flask_sqlalchemy import SQLAlchemy" in content
    assert "db = SQLAlchemy()" in content
    assert f"{TAB}{TAB}db.init_app(app)" in content
    assert f"{TAB}{TAB}db.create_all()" in content

    # Check that config.py contains needed lines
    with open(os.path.join("src", "config.py"), "r+") as f:
        content = f.read().split("\n")

    assert f'{TAB}SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")' in content
    assert f"{TAB}SQLALCHEMY_TRACK_MODIFICATIONS = False" in content

    # Call uninstall
    FlaskSQLAlchemyInstaller.uninstall()

    # Check that models directory doesn't exist
    assert not os.path.exists(os.path.join("src", "models"))
    assert not os.path.exists(os.path.join("src", "models", "__init__.py"))

    # Check that __init__.py doesn't contain associated lines
    with open(os.path.join("src", "__init__.py"), "r") as f:
        content = f.read().split("\n")

    assert "from flask_sqlalchemy import SQLAlchemy" not in content
    assert "db = SQLAlchemy()" not in content
    assert f"{TAB}{TAB}db.init_app(app)" not in content
    assert f"{TAB}{TAB}db.create_all()" not in content

    # Check that config.py doesn't contain associated lines
    with open(os.path.join("src", "config.py"), "r") as f:
        content = f.read().split("\n")

    assert f'{TAB}SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")' not in content
    assert f"{TAB}SQLALCHEMY_TRACK_MODIFICATIONS = False" not in content

from ..conf_tests import app, cli
from flask_boot import install
from flask_boot.installers import FlaskSQLAlchemyInstaller
import os


def test_flask_sqlalchemy_installer(app, cli):
    # Install the extension
    FlaskSQLAlchemyInstaller.install()

    # Check that models directory exists
    assert os.path.exists("src/models")
    assert os.path.exists("src/models/__init__.py")

    # Check that __init__.py contains needed lines
    with open("src/__init__.py", "r") as f:
        content = f.read().split("\n")
        print(content)

    assert "from flask_sqlalchemy import SQLAlchemy" in content
    assert "db = SQLAlchemy()" in content
    assert "\t\tdb.init_app(app)" in content
    assert "\t\tdb.create_all()" in content

    # Check that config.py contains needed lines
    with open("src/config.py", "r+") as f:
        content = f.read().split("\n")

    assert '\tSQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")' in content
    assert "\tSQLALCHEMY_TRACK_MODIFICATIONS = False" in content

    # Call uninstall
    FlaskSQLAlchemyInstaller.uninstall()

    # Check that models directory doesn't exist
    assert not os.path.exists("src/models")
    assert not os.path.exists("src/models/__init__.py")

    # Check that __init__.py doesn't contain associated lines
    with open("src/__init__.py", "r") as f:
        content = f.read().split("\n")

    assert "from flask_sqlalchemy import SQLAlchemy" not in content
    assert "db = SQLAlchemy()" not in content
    assert "\t\tdb.init_app(app)" not in content
    assert "\t\tdb.create_all()" not in content

    # Check that config.py doesn't contain associated lines
    with open("src/config.py", "r") as f:
        content = f.read().split("\n")

    assert '\tSQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")' not in content
    assert "\tSQLALCHEMY_TRACK_MODIFICATIONS = False" not in content

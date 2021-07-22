from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskMigrateInstaller
import os
from flask_batteries.config import TAB


def test_flask_migrate_installer(app, cli):
    assert FlaskMigrateInstaller.verify()

    # Call uninstall
    result = cli.invoke(uninstall, "migrate")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Check that models directory doesn't exist
    assert not os.path.exists(os.path.join("src", "migrations"))

    # Check that __init__.py doesn't contain associated lines
    with open(os.path.join("src", "__init__.py"), "r") as f:
        content = f.read().split("\n")

    assert "from flask_migrate import Migrate" not in content
    assert 'migrate = Migrate(db, directory="src/migrations")' not in content
    assert f"{TAB}{TAB}migrate.init_app(app)" not in content

    assert not FlaskMigrateInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "migrate")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Check that migrations directory exists
    assert os.path.exists(os.path.join("src", "migrations"))

    # Check that __init__.py contains needed lines
    with open(os.path.join("src", "__init__.py"), "r") as f:
        content = f.read().split("\n")

    assert "from flask_migrate import Migrate" in content
    assert 'migrate = Migrate(db, directory="src/migrations")' in content
    assert f"{TAB}{TAB}migrate.init_app(app)" in content

    assert FlaskMigrateInstaller.verify()

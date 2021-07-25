from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskLoginInstaller
import os
from flask_batteries.config import TAB
import traceback

def test_flask_login_installer(app, cli):
    assert not FlaskLoginInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "login")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert FlaskLoginInstaller.verify()

    with open(os.path.join("src", "__init__.py")) as f:
        content = f.read()
        assert "@login_manager.user_loader" in content

    # Call uninstall
    result = cli.invoke(uninstall, "login")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    with open(os.path.join("src", "__init__.py")) as f:
        content = f.read()
        assert "@login_manager.user_loader" not in content


    assert not FlaskLoginInstaller.verify()

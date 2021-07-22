from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskWTFInstaller
import os
from flask_batteries.config import TAB


def test_flask_wtf_installer(app, cli):
    assert not FlaskWTFInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "wtf")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Check that forms directory exists
    assert os.path.exists(os.path.join("src", "forms"))
    assert os.path.exists(os.path.join("src", "forms", "__init__.py"))

    assert FlaskWTFInstaller.verify()

    # Call uninstall
    result = cli.invoke(uninstall, "wtf")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Check that forms directory doesn't exist
    assert not os.path.exists(os.path.join("src", "forms"))
    assert not os.path.exists(os.path.join("src", "forms", "__init__.py"))

    assert not FlaskWTFInstaller.verify()

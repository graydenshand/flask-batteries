from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskBabelInstaller
import os
from flask_batteries.config import TAB
import traceback


def test_flask_babel_installer(app, cli):
    assert not FlaskBabelInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "babel")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert FlaskBabelInstaller.verify(raise_for_error=True)

    # Call uninstall
    result = cli.invoke(uninstall, "babel")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not FlaskBabelInstaller.verify()

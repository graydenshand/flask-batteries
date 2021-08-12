from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskTalismanInstaller
import os
from flask_batteries.config import TAB
import traceback


def test_flask_talisman_installer(app, cli):
    assert not FlaskTalismanInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "talisman")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert FlaskTalismanInstaller.verify(raise_for_error=True)

    # Call uninstall
    result = cli.invoke(uninstall, "talisman")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not FlaskTalismanInstaller.verify()

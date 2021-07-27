from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskMailInstaller
import os
from flask_batteries.config import TAB
import traceback


def test_flask_mail_installer(app, cli):
    assert not FlaskMailInstaller.verify()

    # Install the extension
    result = cli.invoke(install, "mail")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert FlaskMailInstaller.verify()

    # Call uninstall
    result = cli.invoke(uninstall, "mail")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not FlaskMailInstaller.verify()

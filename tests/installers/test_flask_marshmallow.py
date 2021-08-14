from ..conf_tests import app, cli
from flask_batteries.commands import install, uninstall
from flask_batteries.installers import FlaskMarshmallowInstaller
import os
import traceback


def test_flask_marshmallow_installer(app, cli):
    assert FlaskMarshmallowInstaller.verify(raise_for_error=True)

    # Uninstall the extension
    result = cli.invoke(uninstall, "marshmallow")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not FlaskMarshmallowInstaller.verify()

    # Call install
    result = cli.invoke(install, "marshmallow")
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert FlaskMarshmallowInstaller.verify(raise_for_error=True)

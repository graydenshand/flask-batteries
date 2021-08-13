from ..conf_tests import cli, app
from flask_batteries.commands import install, translate
from flask_batteries.installers import FlaskBabelInstaller
import traceback
import os


def test_translate_commands(cli, app):
    cli.invoke(install, ["babel"])
    assert FlaskBabelInstaller.verify(raise_for_error=True)

    result = cli.invoke(translate, ["init", "es", "-k", "_l"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert os.path.exists(
        os.path.join("src", "translations", "es", "LC_MESSAGES", "messages.po")
    )

    result = cli.invoke(translate, ["update", "-k", "_l", "-k", "_lazy"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    result = cli.invoke(translate, ["compile"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert os.path.exists(
        os.path.join("src", "translations", "es", "LC_MESSAGES", "messages.mo")
    )


def test_translate_commands_are_hidden_by_default(cli, app):
    result = cli.invoke(translate, ["init", "es"])
    assert result.exit_code != 0

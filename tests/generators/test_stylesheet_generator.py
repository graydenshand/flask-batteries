from ..conf_tests import app, cli
from flask_batteries.commands import new, generate, destroy
import os
import traceback
from flask_batteries.config import TAB
from flask_batteries.helpers import activate
import subprocess


def test_stylesheet_generator(cli, app):
    # Generate file
    result = cli.invoke(generate, ["stylesheet", "typography"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert os.path.exists(
        os.path.join("src", "assets", "stylesheets", "_typography.scss")
    )
    with open(os.path.join("src", "assets", "stylesheets", "styles.scss"), "r") as f:
        content = f.read()
        assert "@use 'typography'" in content

    # Destroy generated files
    result = cli.invoke(destroy, ["stylesheet", "typography"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not os.path.exists(
        os.path.join("src", "assets", "stylesheets", "_typography.scss")
    )
    with open(os.path.join("src", "assets", "stylesheets", "styles.scss"), "r") as f:
        content = f.read()
        assert "@use 'typography'" not in content


def test_stylesheet_generator_without_webpack(cli):
    # Create a new app without webpack integration
    result = cli.invoke(new, ["app", "--skip-webpack"])

    # Generate file
    result = cli.invoke(generate, ["stylesheet", "typography"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert os.path.exists(
        os.path.join("src", "static", "stylesheets", "typography.css")
    )

    result = cli.invoke(destroy, ["stylesheet", "typography"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert not os.path.exists(
        os.path.join("src", "static", "stylesheets", "typography.css")
    )

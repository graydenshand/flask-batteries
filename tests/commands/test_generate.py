from ..conf_tests import app, cli, stylesheet
from flask_batteries.commands import new, generate
import os
import traceback
from flask_batteries.config import TAB
from flask_batteries.helpers import activate
import subprocess


def test_generate_route(cli, app):
    result = cli.invoke(generate, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" in content
        assert f'{TAB}app.add_url_rule("/sign-up/", view_func=sign_up_view)' in content


def test_generate_stylesheet(cli, app, stylesheet):
    assert os.path.exists(
        os.path.join("src", "assets", "stylesheets", "typography.scss")
    )
    with open(os.path.join("src", "assets", "stylesheets", "styles.scss"), "r") as f:
        content = f.read()
        assert "@use 'typography'" in content


def test_generate_stylesheet_without_webpack(cli):
    """
    Must run this command in subprocess, as it relies
    on an active context from the generated app.
    """
    result = cli.invoke(new, ["--skip-webpack"])
    if os.name != "nt":
        result = subprocess.run(
            f"source {activate()} && flask generate stylesheet typography", shell=True
        )
    else:
        result = subprocess.run(
            f"{activate().rstrip('.bat')} && flask generate stylesheet typography",
            shell=True,
        )
    assert result.returncode == 0, result.stdout
    assert os.path.exists(
        os.path.join("src", "static", "stylesheets", "typography.css")
    )

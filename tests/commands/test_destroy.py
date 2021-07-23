from ..conf_tests import app, route, cli, stylesheet
from flask_batteries.commands import new, destroy
import os
import traceback
from flask_batteries.helpers import activate
import subprocess


def test_destroy_route_destroys_correct_files(cli, route, app):
    result = cli.invoke(destroy, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert not os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert not os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert not os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import SignUp" not in content
        assert (
            '\tapp.add_url_rule("/sign-up/", view_func=SignUp.as_view("sign_up"))'
            not in content
        )


def test_destroy_stylesheet(cli, app, stylesheet):
    """
    Must run this command in subprocess, as it relies
    on an active context from the generated app.
    """
    if os.name != "nt":
        result = subprocess.run(
            f"source {activate()} && flask destroy stylesheet typography", shell=True
        )
    else:
        result = subprocess.run(
            f"{activate().rstrip('.bat')} && flask destroy stylesheet typography",
            shell=True,
        )
    assert not os.path.exists(
        os.path.join("src", "assets", "stylesheets", "typography.scss")
    )
    with open(os.path.join("src", "assets", "stylesheets", "styles.scss"), "r") as f:
        content = f.read()
        assert "@use 'typography'" not in content


def test_destroy_stylesheet_without_webpack(cli):
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
    if os.name != "nt":
        result = subprocess.run(
            f"source {activate()} && flask destroy stylesheet typography", shell=True
        )
    else:
        result = subprocess.run(
            f"{activate().rstrip('.bat')} && flask destroy stylesheet typography",
            shell=True,
        )
    assert not os.path.exists(
        os.path.join("src", "static", "stylesheets", "typography.css")
    )

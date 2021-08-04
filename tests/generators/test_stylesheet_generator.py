from ..conf_tests import app, cli
from flask_batteries.commands import new, generate
import os
import traceback
from flask_batteries.config import TAB
from flask_batteries.helpers import activate
import subprocess


def test_stylesheet_generator(cli, app):
    """
    Generate files

    Must run this command in subprocess, as it relies
    on an active context from the generated app.
    """
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
        os.path.join("src", "assets", "stylesheets", "typography.scss")
    )
    with open(os.path.join("src", "assets", "stylesheets", "styles.scss"), "r") as f:
        content = f.read()
        assert "@use 'typography'" in content

    """
    Destroy generated files
    
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


def test_stylesheet_generator_without_webpack(cli):
    """
    Generate files

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

    """
    Destroy generated files 

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

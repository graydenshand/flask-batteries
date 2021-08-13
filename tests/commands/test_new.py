from flask_batteries.commands import new
from click.testing import CliRunner
from ..conf_tests import cli, app
import os
from pkg_resources import resource_filename
import re
import subprocess
import pathspec
import traceback
from flask_batteries.helpers import activate
from flask_batteries.installers import FlaskSQLAlchemyInstaller, FlaskMigrateInstaller


def test_new_doesnt_fail(cli):
    result = cli.invoke(new)
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)


def test_new_creates_all_resources_in_template_directory(cli, app):
    # Walk the app template and verify every file and directory was copied
    with open(resource_filename("flask_batteries", "template/.gitignore"), "r") as f:
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    ignore_matches = list(
        ignore_spec.match_tree(resource_filename("flask_batteries", "template"))
    )
    for dirpath, dirs, files in os.walk(
        resource_filename("flask_batteries", "template")
    ):
        pattern = r"template[\/]*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            if d != "__pycache__":
                resource = os.path.join(path, d).lstrip("\\") if path else d
                assert os.path.exists(resource)
        for f in files:
            resource = os.path.join(path, f).lstrip("\\") if path else f
            if resource not in ignore_matches:
                assert os.path.exists(resource)


def test_generated_app_passes_all_generated_tests(cli, app):
    # Run the generated app's test suite and verify exit code is 0
    if os.name != "nt":
        run_tests = subprocess.run("source venv/bin/activate && pytest", shell=True)
    else:
        run_tests = subprocess.run("venv\\Scripts\\activate && pytest", shell=True)
    assert run_tests.returncode == 0, run_tests.stdout


def test_new_with_path_to_venv_option_doesnt_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("app")
        os.chdir("app")
        subprocess.run(["python", "-m", "venv", ".venv"])
        result = runner.invoke(new, ["--path-to-venv", ".venv"])
        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)


def test_new_with_skip_webpack(cli):
    result = cli.invoke(new, ["--skip-webpack"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert not os.path.exists("webpack.config.js")
    assert not os.path.exists(os.path.join("src", "assets"))
    assert os.path.exists(os.path.join("src", "static", "images", "flask-logo.png"))
    assert os.path.exists(os.path.join("src", "static", "images", "flask-icon.png"))
    assert os.path.exists(os.path.join("src", "static", "stylesheets", "base.css"))
    assert os.path.exists(os.path.join("src", "static", "javascript"))

    with open(os.path.join("src", "config.py"), "r") as f:
        content = f.read()
        assert "BATTERIES_USE_WEBPACK" in content

    if os.name != "nt":
        run_tests = subprocess.run("source venv/bin/activate && pytest", shell=True)
    else:
        run_tests = subprocess.run("venv\\Scripts\\activate && pytest", shell=True)
    assert run_tests.returncode == 0, run_tests.stdout


def test_new_with_git_branch(cli):
    result = cli.invoke(new, ["--git-initial-branch", "primary"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    subprocess.run("git add . && git commit -m '.'", shell=True, check=True)

    branches = subprocess.check_output("git branch", shell=True)
    assert branches == b"* primary\n"


def test_new_with_skip_db(cli):
    result = cli.invoke(new, ["--skip-db"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert not FlaskSQLAlchemyInstaller.verify()
    assert not FlaskMigrateInstaller.verify()

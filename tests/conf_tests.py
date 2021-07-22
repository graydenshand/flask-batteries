import pytest
from click.testing import CliRunner
from flask_batteries.commands import new, generate
import subprocess
import os
import shutil
import traceback


@pytest.fixture()
def cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("app")
        os.chdir("app")
        subprocess.run(["python", "-m", "venv", "venv"])
        yield runner


@pytest.fixture()
def app(cli):
    result = cli.invoke(new)
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)


@pytest.fixture
def route(cli, app):
    result = cli.invoke(generate, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

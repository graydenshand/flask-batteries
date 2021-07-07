import pytest
from click.testing import CliRunner
from flask_batteries import new, generate
import subprocess
import os


@pytest.fixture
def cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("app")
        os.chdir("app")
        subprocess.run("python3 -m venv venv", shell=True)
        yield runner


@pytest.fixture
def app(cli):
    cli.invoke(new)


@pytest.fixture
def route(cli):
    cli.invoke(generate, ["route", "sign_up"])
    return

import pytest
from click.testing import CliRunner
from flask_batteries.commands import new, generate
import subprocess
import os
import shutil


@pytest.fixture(scope="session")
def cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("app")
        os.chdir("app")
        subprocess.run("python -m venv venv", shell=True)
        yield runner
        os.chdir("..")
        shutil.rmtree("app")


@pytest.fixture(scope="session")
def app(cli):
    cli.invoke(new)


@pytest.fixture
def route(cli):
    cli.invoke(generate, ["route", "sign_up"])
    return

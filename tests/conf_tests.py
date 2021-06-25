import pytest
from click.testing import CliRunner
from flask_boot import new


@pytest.fixture
def cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


@pytest.fixture
def app(cli):
    cli.invoke(new, "app")

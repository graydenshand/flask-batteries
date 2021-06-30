from ..fixtures import client, app, cli
from src.commands import build

def test_build_command_runs_without_failure(cli):
    # Run the generated app's test suite and verify exit code is 0
    result = cli.invoke(build, ['--bail'])
    assert result.exit_code == 0

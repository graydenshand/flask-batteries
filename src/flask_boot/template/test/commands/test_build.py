from ..fixtures import client, app
import subprocess
from src.commands import build

def test_build_command_runs_without_failure():
    # Run the generated app's test suite and verify exit code is 0
    run_webpack = subprocess.run("flask build --bail", shell=True)
    assert run_webpack.returncode == 0, run_webpack.stdout

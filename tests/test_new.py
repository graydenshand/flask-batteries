from flask_boot import new
from .conf_tests import cli, app
import os
from pkg_resources import resource_filename
import re
import subprocess

def test_new_doesnt_fail(cli):
	result = cli.invoke(new, "app")
	assert result.exit_code == 0

def test_new_creates_all_resources_in_template_directory(cli, app):
	# Walk the app template and verify every file and directory was copied
	for dirpath, dirs, files in os.walk(resource_filename("flask_boot", "template")):
		pattern = r"template\/*(.*)"
		match = re.search(pattern, dirpath)
		path = match.group(1)
		for d in dirs:
			resource = "./" + path + "/" + d if path else d
			if "__pycache__" not in resource:
				assert os.path.exists(resource)
		for f in files:
			resource = "./" + path + "/" + f if path else f
			if "__pycache__" not in resource:
				assert os.path.exists(resource)

def test_generated_app_passes_all_generated_tests(cli, app):
	# Run the generated app's test suite and verify exit code is 0
	run_tests = subprocess.run("source venv/bin/activate && pytest", shell=True)
	assert run_tests.returncode == 0, run_tests.stdout
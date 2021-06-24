from flask_boot import new
from .conf_tests import cli, app
import os

def test_new_doesnt_fail(cli):
	result = cli.invoke(new, "app")
	assert result.exit_code == 0

def file_exists(filename, directory="."):
	for dirpath, dirs, files in os.walk("."):
		if filename in files and dirpath == directory:
			return True
	return False

def directory_exists(dirname, directory="."):
	for dirpath, dirs, files in os.walk("."):
		if dirname in dirs and dirpath == directory:
			return True
	return False

def test_new_creates_correct_file_structure(cli, app):
	structure = {
		".": [
			".gitignore",
			"README.md",
			"main.py",
		], 
		"./src": [
			"__init__.py",
			"config.py"
		],
		"./src/templates": [],
		"./src/static": [],
		"./src/routes": [
			"__init__.py"
		],
		"./src/models": [
			"__init__.py"
		],
		"./src/blueprints": [],
		"./tests": [],
	}

	for dirpath, dirs, files in os.walk("."):
		if dirpath in structure.keys():
			if structure[dirpath] == []:
				# Handle case where directory contains no files
				del structure[dirpath]
			else:
				for file in files:
					# Delete all files in directory
					idx = structure[dirpath].index(file)
					del structure[dirpath][idx]
				assert structure[dirpath] == [], f"Found missing file(s) in generated file structure: {structure[dirpath]}"
				# Delete directory
				del structure[dirpath]

	# Assert all files in file structure have been accounted for
	assert structure == {}, f"Objects missing from generated file structure: {structure}"
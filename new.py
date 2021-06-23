#!/opt/homebrew/bin/python3
import os
import sys
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import subprocess

name = sys.argv[1].lower()

print("Generating new app named: %s" % name)

# Create empty directory and set it as current working directory
os.mkdir(name)
os.chdir(name)

# Create top level directories
os.mkdir("src")
os.mkdir("tests")
os.mkdir("src/models")
os.mkdir("src/templates")
os.mkdir("src/static")
os.mkdir("src/routes")
os.mkdir("src/blueprints")

env = Environment(
	loader=FileSystemLoader('../template'),
	autoescape=select_autoescape()
)

def render_template(filename, **params):
	template = env.get_template(filename)
	return template.render(**params)

def copy_template(filename, **params):
	with open(filename, "w") as f:
		f.write(
			render_template(filename, **params)
		)
	return

def set_env_vars(skip_check=False, **kwargs):
	# Add an environment variable to venv/bin/activate
	if skip_check:
		with open("venv/bin/activate", "a") as f:
			for key,val in kwargs.items():
				f.write(f"export {key}={val}\n")
		return
	else:
		with open("venv/bin/activate", "r") as f:
			# Get existing file content
			body = f.read()

		with open("venv/bin/activate", "w") as f:
			# If key is already specified, remove it
			for key,val in kwargs.items():
				regex = f"export {key}={val}\n"
				body = re.sub(regex, "", body) + f"export {key}={val}\n"
				f.write(body)
		return

# Create README.md
copy_template("README.md", name=name[0].upper() + name[1:])

# Create .gitignore, set up git repo
copy_template(".gitignore")
subprocess.run(['git', 'init'])

# Create main.py
copy_template("main.py")

# Set up virtual env
subprocess.run(["python3", "-m", "venv", "venv"])
## Install requirements
subprocess.run([f'venv/bin/pip', 'install', 'flask'])
## Set default environment variables
envs = {
	"FLASK_APP": "main.py",
	"FLASK_ENV": "development"
}
set_env_vars(skip_check=True, **envs)


# Copy files in src directory
copy_template("src/__init__.py")
copy_template("src/config.py")

# Copy files in routes directory
copy_template("src/routes/__init__.py")

# Copy files in models directory
copy_template("src/models/__init__.py")
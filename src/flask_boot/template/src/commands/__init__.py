from .build import build
from .watch import watch

def register_commands(app):
	app.cli.add_command(build)
	app.cli.add_command(watch)
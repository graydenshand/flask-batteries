from .build import build
from .watch import watch
from .generate import generate
from .destroy import destroy
from .rename import rename

def register_commands(app):
	app.cli.add_command(build)
	app.cli.add_command(watch)
	app.cli.add_command(generate)
	app.cli.add_command(destroy)
	app.cli.add_command(rename)
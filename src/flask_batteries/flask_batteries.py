from .webpack import webpack_init
from .commands import *

class Batteries(object):

	def __init__(self, app):
		webpack_init(app)

		app.cli.add_command(destroy)
		app.cli.add_command(generate)
		app.cli.add_command(install)
		app.cli.add_command(new)
		app.cli.add_command(uninstall)
		app.cli.add_command(webpack)


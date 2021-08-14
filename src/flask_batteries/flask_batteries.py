from .webpack import webpack_init
from .commands import *
from .commands.generate import model as generate_model
from .commands.destroy import model as destroy_model
from .commands import generate, destroy
import os


class Batteries(object):
    def __init__(self, app):
        app.cli.add_command(destroy)
        app.cli.add_command(generate)
        app.cli.add_command(install)
        app.cli.add_command(new)
        app.cli.add_command(uninstall)

        if app.config.get("BATTERIES_USE_WEBPACK") != False:
            webpack_init(app)
            app.cli.add_command(webpack)

        if app.config.get("BATTERIES_USE_BABEL") == True:
            app.cli.add_command(translate)

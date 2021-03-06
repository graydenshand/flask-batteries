"""
This file is automatically generated by Flask-Batteries. 

Do not remove the --flask_batteries_mar XXXXXX-- lines. 
These lines are used by Flask-Batteries when installing extensions.
"""


from flask import Flask, url_for
from .config import ProductionConfig
from .routes import register_routes
import subprocess
import requests
from flask_batteries import Batteries

# --flask_batteries_mark imports--

# --flask_batteries_mark initializations--

# Create app
def create_app(config=ProductionConfig):
    app = Flask(__name__)

    with app.app_context():
        # Load app config
        app.config.from_object(config)

        # Register routes
        register_routes(app)

        Batteries(app)
        # --flask_batteries_mark attachments--

        @app.shell_context_processor
        def inject_variables_into_shell_context():
            """
            Return a dictionary containing items that you wish to
            use in your `flask shell` environment.
            """
            return {
                # --flask_batteries_mark shell_vars--
            }

        @app.context_processor
        def inject_global_template_variables():
            """
            Return a dictionary containing items that you wish to
            have available in every template
            """
            return {}

    return app

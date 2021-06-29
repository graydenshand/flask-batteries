from flask import Flask
from .config import ProductionConfig
from .routes import register_routes
from .commands import register_commands
from .helpers import webpack_init
import subprocess
import requests
from .helpers import static_url_for


def create_app(config=ProductionConfig):
    app = Flask(__name__)

    with app.app_context():
        # Load app config
        app.config.from_object(config)

        # Register routes
        register_routes(app)

        # Register commands
        register_commands(app)

        # Initialize webpack helpers
        if app.config["ENV"] == "development":
            webpack_init(app)

        @app.shell_context_processor
        def inject_variables_into_shell_context():
            return {}

        @app.context_processor
        def inject_global_template_variables():
            return {"application_name": "{{name}}", "app": app, "static_url_for": static_url_for}
        
    return app

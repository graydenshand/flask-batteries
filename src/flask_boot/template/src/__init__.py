from flask import Flask
from .config import ProductionConfig
from .routes import *


def create_app(config=ProductionConfig):
    app = Flask(__name__)

    with app.app_context():
        # Load app config
        app.config.from_object(config)

        # Register routes
        app.add_url_rule("/", view_func=index)

        @app.shell_context_processor
        def make_shell_context():
            return {}

        @app.context_processor
        def inject_global_template_variables():
            return {"application_name": "{{name}}", "app": app}

    return app

from flask import Flask
from .config import ProductionConfig
from .routes import *
import subprocess
import requests
from .helpers import static_url_for


def create_app(config=ProductionConfig):
    app = Flask(__name__)

    with app.app_context():
        # Load app config
        app.config.from_object(config)

        # Register routes
        app.add_url_rule("/", view_func=index)

        @app.shell_context_processor
        def inject_variables_into_shell_context():
            return {}

        @app.context_processor
        def inject_global_template_variables():
            return {"application_name": "{{name}}", "app": app}

        if app.config["ENV"] == "development":

            @app.before_first_request
            def build_assets_on_reload_if_webpack_dev_server_not_running():
                global USE_WEBPACK_DEV_SERVER
                if app.config["ENV"] == "development":
                    try:
                        r = requests.get("http://localhost:3000/static/main.js")
                        # Webpack dev server is running
                        app.config['USE_WEBPACK_DEV_SERVER'] = True
                    except requests.exceptions.ConnectionError as e:
                        # Webpack dev server is not running
                        app.logger.warn(
                            "Compiling static assets. To avoid this warning, start the webpack dev server in a new shell with `npx webpack serve`."
                        )
                        app.config['USE_WEBPACK_DEV_SERVER'] = False
                        subprocess.run("npx webpack", shell=True)

            @app.before_request
            def webpack_dev_server_health_check():
                global USE_WEBPACK_DEV_SERVER
                if app.config["ENV"] == "development":
                    try:
                        r = requests.get("http://localhost:3000/static/main.js")
                        # Webpack dev server is running
                        app.config['USE_WEBPACK_DEV_SERVER'] = True
                    except requests.exceptions.ConnectionError as e:
                        # Webpack dev server is not running
                        app.config['USE_WEBPACK_DEV_SERVER'] = False

        @app.context_processor
        def inject_global_template_variables():
            global USE_WEBPACK_DEV_SERVER
            return {
                "application_name": "flask_boot_test",
                "app": app,
                #"use_webpack_dev_server": USE_WEBPACK_DEV_SERVER,
                "static_url_for": static_url_for
            }

        # Register commands
        from .commands import build
        app.cli.add_command(build)

    return app

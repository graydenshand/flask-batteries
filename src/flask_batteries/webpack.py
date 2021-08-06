"""
Functions for working with webpack

Use webpack_init(app) to attach dev tools and template vars to an application instance
"""

import requests
from flask import current_app, url_for
import subprocess
import os


def static_url_for(path):
    if current_app.config["USE_WEBPACK_DEV_SERVER"]:
        return f"http://localhost:3000/static/{path}"
    else:
        return url_for("static", filename=path)


def webpack_init(app):
    if app.config["ENV"] == "development":

        @app.before_first_request
        def build_assets_on_reload_if_webpack_dev_server_not_running():
            try:
                r = requests.get("http://localhost:3000/static/main.js")
                # Webpack dev server is running
                app.config["USE_WEBPACK_DEV_SERVER"] = True
            except requests.exceptions.ConnectionError as e:
                # Webpack dev server is not running
                app.logger.warning(
                    "Compiling static assets. To avoid this warning, start the webpack dev server in a new shell with `flask webpack watch`."
                )
                app.config["USE_WEBPACK_DEV_SERVER"] = False
                subprocess.run("npx webpack", shell=True)

        @app.before_request
        def webpack_dev_server_health_check():
            try:
                r = requests.get("http://localhost:3000/static/main.js")
                # Webpack dev server is running
                app.config["USE_WEBPACK_DEV_SERVER"] = True
            except requests.exceptions.ConnectionError as e:
                # Webpack dev server is not running
                app.config["USE_WEBPACK_DEV_SERVER"] = False

        # Add all files in ./src/assets directory to watched files list
        extra_files = []
        watched_directories = ["./src/assets"]
        for directory in watched_directories:
            for dirpath, dirs, files in os.walk(directory):
                for filename in files:
                    filename = os.path.join(dirpath, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
        if os.name != 'nt':
            os.environ["FLASK_RUN_EXTRA_FILES"] = ":".join(extra_files)
        else:
            os.environ["FLASK_RUN_EXTRA_FILES"] = ";".join(extra_files)



    @app.context_processor
    def webpack_init_template_vars():
        return {"static_url_for": static_url_for}

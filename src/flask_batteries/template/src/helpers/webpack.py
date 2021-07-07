import requests
from flask import current_app, url_for
import subprocess


def static_url_for(path):
    if current_app.config["USE_WEBPACK_DEV_SERVER"]:
        return f"http://localhost:3000/static/{path}"
    else:
        return url_for("static", filename=path)


def webpack_init(app):
    @app.before_first_request
    def build_assets_on_reload_if_webpack_dev_server_not_running():
        if app.config["ENV"] == "development":
            try:
                r = requests.get("http://localhost:3000/static/main.js")
                # Webpack dev server is running
                app.config["USE_WEBPACK_DEV_SERVER"] = True
            except requests.exceptions.ConnectionError as e:
                # Webpack dev server is not running
                app.logger.warn(
                    "Compiling static assets. To avoid this warning, start the webpack dev server in a new shell with `flask watch`."
                )
                app.config["USE_WEBPACK_DEV_SERVER"] = False
                subprocess.run("npx webpack", shell=True)

    @app.before_request
    def webpack_dev_server_health_check():
        if app.config["ENV"] == "development":
            try:
                r = requests.get("http://localhost:3000/static/main.js")
                # Webpack dev server is running
                app.config["USE_WEBPACK_DEV_SERVER"] = True
            except requests.exceptions.ConnectionError as e:
                # Webpack dev server is not running
                app.config["USE_WEBPACK_DEV_SERVER"] = False

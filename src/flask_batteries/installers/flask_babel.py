from .base_installer import FlaskExtInstaller, InstallError
from ..helpers import TAB
import os
import shutil
import re


class FlaskBabelInstaller(FlaskExtInstaller):
    package_name = "Flask-Babel"
    imports = ["from flask_babel import Babel"]
    inits = ["babel = Babel()"]
    attachments = ["babel.init_app(app)"]
    decorators = [
        "@babel.localeselector",
        "def get_locale():",
        f"{TAB}return request.accept_languages.best_match(app.config['LANGUAGES'])",
    ]
    base_config = {
        "LANGUAGES": '["en"]',
    }
    development_config = {"BATTERIES_USE_BABEL": "True"}

    @classmethod
    def install(cls):
        super().install()
        # Create a 'translations' folder if one does not exist
        if not os.path.exists(os.path.join("src", "translations")):
            os.mkdir(os.path.join("src", "translations"))

        if not os.path.exists(os.path.join("babel.cfg")):
            lines = [
                "[python: src/**.py]",
                "[jinja2: src/**/templates/**.html]",
                "extensions=jinja2.ext.autoescape,jinja2.ext.with_",
            ]
            with open(os.path.join("babel.cfg"), "w+") as f:
                f.write("\n".join(lines))

        with open(os.path.join("src", "__init__.py"), "r+") as f:
            content = f.read()
            pattern = r"(from flask import .*)\n"
            content = re.sub(pattern, "\g<1>, request\n", content)
            f.seek(0)
            f.truncate()
            f.write(content)

    @classmethod
    def uninstall(cls):
        super().uninstall()
        # Delete translations folder
        if os.path.exists(os.path.join("src", "translations")):
            shutil.rmtree(os.path.join("src", "translations"))

        if os.path.exists(os.path.join("src", "babel.cfg")):
            os.remove(os.path.join("src", "babel.cfg"))

    @classmethod
    def verify(cls, raise_for_error=False):
        if not os.path.exists(
            os.path.join("src", "translations")
        ) or not os.path.exists(os.path.join("babel.cfg")):
            if raise_for_error:
                raise InstallError(
                    "Missing files in Flask-Babel installation. Check src/translations and babel.cfg"
                )
            return False
        else:
            return super().verify(raise_for_error=raise_for_error)

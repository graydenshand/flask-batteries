from .base_installer import FlaskExtInstaller
from ..helpers import TAB


class FlaskTalismanInstaller(FlaskExtInstaller):
    package_name = "Flask-Talisman"
    imports = ["from flask_talisman import Talisman"]
    inits = ["talisman = Talisman()"]
    attachments = [
        'force_https = True if app.config.get("ENV") != "testing" else False',
        "talisman.init_app(",
        f"{TAB}app,",
        f"{TAB}force_https=force_https",
        ")",
    ]

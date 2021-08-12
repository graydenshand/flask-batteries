from .base_installer import FlaskExtInstaller
from ..config import TAB
import os
import shutil


class FlaskMailInstaller(FlaskExtInstaller):
    package_name = "Flask-Mail"
    imports = ["from flask_mail import Mail"]
    inits = ["mail = Mail()"]
    attachments = ["mail.init_app(app)"]

    base_config = [
        "# Flask-Mail",
        'MAIL_SERVER = "localhost"',
        "MAIL_PORT = 25",
        "MAIL_USE_TLS = False",
        "MAIL_USE_SSL = False",
        "MAIL_USERNAME = None",
        "MAIL_PASSWORD = None",
        "MAIL_DEFAULT_SENDER = None",
    ]

    @classmethod
    def install(cls):
        """
        Extend default install function by creating a 'mail' folder in 'src/templates'
        """
        super().install()

        if not os.path.exists(os.path.join("src", "templates", "mail")):
            os.mkdir(os.path.join("src", "templates", "mail"))

    @classmethod
    def uninstall(cls):
        """
        Extend default uninstall function by deleting the 'mail' folder in 'src/templates'
        """
        super().uninstall()

        if os.path.exists(os.path.join("src", "templates", "mail")):
            shutil.rmtree(os.path.join("src", "templates", "mail"))

    @classmethod
    def verify(cls, raise_for_error=False):
        """
        Extend default verify function by verifying 'mail' folder in 'src/templates'
        """
        if not os.path.exists(os.path.join("src", "templates", "mail")):
            return False
        else:
            return super().verify()

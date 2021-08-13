from .base_installer import FlaskExtInstaller
import os
from ..config import TAB


class FlaskLoginInstaller(FlaskExtInstaller):
    package_name = "Flask-Login"
    imports = ["from flask_login import LoginManager"]
    inits = ["login_manager = LoginManager()"]
    attachments = ["login_manager.init_app(app)"]
    decorators = [
        f"@login_manager.user_loader",
        f"def load_user(user_id):",
        f"{TAB}# For Flask-Login: This callback is used to reload the user object from the user ID stored in the session.",
        f"{TAB}# eg. 'return User.query.get(user_id)'",
        f"{TAB}return",
        "",  # left blank for spacing
    ]

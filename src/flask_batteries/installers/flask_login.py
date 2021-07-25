from .base_installer import FlaskExtInstaller
import os
from ..config import TAB

class FlaskLoginInstaller(FlaskExtInstaller):
    package_name = "Flask-Login"
    imports = ["from flask_login import LoginManager"]
    inits = ["login_manager = LoginManager()"]
    attachments = ["login_manager.init_app(app)"]


    @classmethod
    def install(cls):
        super().install()

        with open(os.path.join("src", "__init__.py"), "r+") as f: 
            lines = f.read().split("\n")

            new_lines = [
                f"{TAB}{TAB}@login_manager.user_loader",
                f"{TAB}{TAB}def load_user(user_id):",
                f"{TAB}{TAB}{TAB}# For Flask-Login: This callback is used to reload the user object from the user ID stored in the session.",
                f"{TAB}{TAB}{TAB}# eg. 'return User.query.get(user_id)'",
                f"{TAB}{TAB}{TAB}return",
                "", # left blank for spacing
            ]

            idx = lines.index(f"{TAB}return app")

            lines = lines[:idx] + new_lines + lines[idx:]

            f.seek(0)
            f.truncate()
            f.write('\n'.join(lines))


    @classmethod
    def uninstall(cls):
        super().uninstall()

        with open(os.path.join("src", "__init__.py"), "r+") as f: 
            lines = f.read().split("\n")

            idx = lines.index(f"{TAB}{TAB}@login_manager.user_loader")
            del lines[idx]
            del lines[idx]
            while f"{TAB}{TAB}{TAB}" in lines[idx]:
                del lines[idx]

            f.seek(0)
            f.truncate()
            f.write('\n'.join(lines))



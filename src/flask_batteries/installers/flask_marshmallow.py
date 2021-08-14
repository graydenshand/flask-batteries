from .base_installer import FlaskExtInstaller
from ..config import TAB


class FlaskMarshmallowInstaller(FlaskExtInstaller):
    package_name = "Flask-Marshmallow"
    pypi_dependencies = ["marshmallow-sqlalchemy"]
    imports = ["from flask_marshmallow import Marshmallow"]
    inits = ["ma = Marshmallow()"]
    attachments = ["ma.init_app(app)"]

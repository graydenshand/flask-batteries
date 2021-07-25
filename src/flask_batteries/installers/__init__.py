from .flask_sqlalchemy import FlaskSQLAlchemyInstaller
from .flask_migrate import FlaskMigrateInstaller
from .flask_wtf import FlaskWTFInstaller
from .flask_login import FlaskLoginInstaller

installers = {
    "sqlalchemy": FlaskSQLAlchemyInstaller,
    "migrate": FlaskMigrateInstaller,
    "wtf": FlaskWTFInstaller,
}

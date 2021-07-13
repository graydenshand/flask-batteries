from .flask_sqlalchemy import FlaskSQLAlchemyInstaller
from .flask_migrate import FlaskMigrateInstaller

installers = {
    "sqlalchemy": FlaskSQLAlchemyInstaller,
    "migrate": FlaskMigrateInstaller,
}

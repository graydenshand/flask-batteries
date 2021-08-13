from .flask_babel import FlaskBabelInstaller
from .flask_login import FlaskLoginInstaller
from .flask_mail import FlaskMailInstaller
from .flask_marshmallow import FlaskMarshmallowInstaller
from .flask_migrate import FlaskMigrateInstaller
from .flask_sqlalchemy import FlaskSQLAlchemyInstaller
from .flask_talisman import FlaskTalismanInstaller
from .flask_wtf import FlaskWTFInstaller
from ..helpers import InstallError


class InstallManager:
    dependencies = {
        FlaskMigrateInstaller: [FlaskSQLAlchemyInstaller],
        FlaskMarshmallowInstaller: [FlaskSQLAlchemyInstaller]
    }

    @classmethod
    def install(cls, installer):
        if installer and not installer.verify():
            dependencies = cls.dependencies.get(installer, [])
            for dep in dependencies:
                if not dep.verify():
                    dep.install()

            installer.install()

    @classmethod
    def uninstall(cls, installer):
        if installer.verify(raise_for_error=True):
            dependents = [
                key for key, val in cls.dependencies.items() if installer in val
            ]

            for dependent, dependencies in cls.dependencies.items():
                if installer in dependencies and dependent.verify():
                    cls.uninstall(dependent)

            installer.uninstall()

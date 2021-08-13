import click
from ..installers import *


@click.group(help="Uninstall a flask extension")
def uninstall():
    pass


@click.command(help="Uninstall Flask-SQLAlchemy")
def sqlalchemy():
    click.echo("Uninstalling Flask-SQLAlchemy")
    InstallManager.uninstall(FlaskSQLAlchemyInstaller)
    click.echo("Done")


uninstall.add_command(sqlalchemy)


@click.command(help="Uninstall Flask-SQLAlchemy")
def migrate():
    click.echo("Uninstalling Flask-Migrate")
    InstallManager.uninstall(FlaskMigrateInstaller)
    click.echo("Done")


uninstall.add_command(migrate)


@click.command(help="Uninstall Flask-WTF")
def wtf():
    click.echo("Uninstalling Flask-WTF")
    InstallManager.uninstall(FlaskWTFInstaller)
    click.echo("Done")


uninstall.add_command(wtf)


@click.command(help="Uninstall Flask-Login")
def login():
    click.echo("Uninstalling Flask-Login")
    InstallManager.uninstall(FlaskLoginInstaller)
    click.echo("Done")


uninstall.add_command(login)


@click.command(help="Uninstall Flask-Mail")
def mail():
    click.echo("Uninstalling Flask-Mail")
    InstallManager.uninstall(FlaskMailInstaller)
    click.echo("Done")


uninstall.add_command(mail)


@click.command(help="Uninstall Flask-Talisman")
def talisman():
    click.echo("Uninstalling Flask-Talisman")
    InstallManager.uninstall(FlaskTalismanInstaller)
    click.echo("Done")


uninstall.add_command(talisman)


@click.command(help="Uninstall Flask-Babel")
def babel():
    click.echo("Uninstalling Flask-Babel")
    InstallManager.uninstall(FlaskBabelInstaller)
    click.echo("Done")


uninstall.add_command(babel)

@click.command(help="Uninstall Flask-Marshmallow")
def marshmallow():
    click.echo("Uninstalling Flask-Marshmallow")
    InstallManager.uninstall(FlaskMarshmallowInstaller)
    click.echo("Done")


uninstall.add_command(marshmallow)

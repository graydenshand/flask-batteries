import click
from ..installers import *


@click.group(help="Uninstall a flask extension")
def uninstall():
    pass


@click.command(help="Uninstall Flask-SQLAlchemy")
def sqlalchemy():
    click.echo("Uninstalling Flask-SQLAlchemy")
    FlaskSQLAlchemyInstaller.uninstall()
    click.echo("Done")


uninstall.add_command(sqlalchemy)


@click.command(help="Uninstall Flask-SQLAlchemy")
def migrate():
    click.echo("Installing Flask-Migrate")
    FlaskMigrateInstaller.uninstall()
    click.echo("Done")


uninstall.add_command(migrate)


@click.command(help="Uninstall Flask-WTF")
def wtf():
    click.echo("Installing Flask-WTF")
    FlaskWTFInstaller.uninstall()
    click.echo("Done")


uninstall.add_command(wtf)


@click.command(help="Uninstall Flask-Login")
def login():
    click.echo("Installing Flask-Login")
    FlaskLoginInstaller.uninstall()
    click.echo("Done")


uninstall.add_command(login)


@click.command(help="Uninstall Flask-Mail")
def mail():
    click.echo("Installing Flask-Mail")
    FlaskMailInstaller.uninstall()
    click.echo("Done")


uninstall.add_command(mail)

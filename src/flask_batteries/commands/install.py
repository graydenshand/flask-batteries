import click
from ..installers import *


@click.group(help="Install a flask extension")
def install():
    pass


@click.command(help="Install Flask-SQLAlchemy")
def sqlalchemy():
    click.echo("Installing Flask-SQLAlchemy")
    FlaskSQLAlchemyInstaller.install()
    click.echo("Done")


install.add_command(sqlalchemy)


@click.command(help="Install Flask-SQLAlchemy")
def migrate():
    click.echo("Installing Flask-Migrate")
    FlaskMigrateInstaller.install()
    click.echo("Done")


install.add_command(migrate)


@click.command(help="Install Flask-WTF")
def wtf():
    click.echo("Installing Flask-WTF")
    FlaskWTFInstaller.install()
    click.echo("Done")


install.add_command(wtf)

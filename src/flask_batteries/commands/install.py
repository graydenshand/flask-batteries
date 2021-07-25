import click
from ..installers import *
from ..config import TAB

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


@click.command(help="Install Flask-Login")
def login():
    click.echo("Installing Flask-Login")
    FlaskLoginInstaller.install()
    click.echo("Done")
    click.echo("Additional configuration steps required:")
    click.echo(f"{TAB}1. Complete \"load_user()\" function in src/__init__.py")

install.add_command(login)
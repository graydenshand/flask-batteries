import click
from ..installers import installers


@click.command(
    help="Install a flask extension. E.g. `flask install sqlalchemy` for Flask-SQLAlchemy"
)
@click.argument("package")
def install(package):
    click.echo(f"Installing flask-{package}")
    installer = installers[package]
    installer.install()
    click.echo("Done")

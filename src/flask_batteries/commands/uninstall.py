import click
from ..installers import installers


@click.command(
    help="Uninstall a flask extension. E.g. `flask uninstall sqlalchemy` for Flask-SQLAlchemy"
)
@click.argument("package")
def uninstall(package):
    # Warn user and confirm deletion
    click.confirm(
        "WARNING: You are about to erase the contents of your `models` directory.\n"
        "Please confirm you would like to uninstall Flask-SQLAlchemy.",
        abort=True,
    )
    click.echo(f"Uninstalling flask-{package}")
    installer = installers[package]
    installer.uninstall()
    click.echo("Done")

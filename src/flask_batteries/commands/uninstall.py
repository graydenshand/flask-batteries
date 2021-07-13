import click
from ..installers import installers


@click.command(
    help="Uninstall a flask extension. E.g. `flask uninstall sqlalchemy` for Flask-SQLAlchemy"
)
@click.argument("package")
def uninstall(package):
    # Warn user and confirm deletion
    click.confirm(
        f"You're about to uninstall flask-{package}. Continue?",
        abort=True,
    )
    click.echo(f"Uninstalling flask-{package}")
    installer = installers[package]
    installer.uninstall()
    click.echo("Done")

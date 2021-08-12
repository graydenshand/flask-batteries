import click
from ..installers import *
from ..config import TAB


@click.group(help="Install a flask extension")
def install():
    pass


@click.command(help="Install Flask-SQLAlchemy")
def sqlalchemy():
    click.echo("Installing Flask-SQLAlchemy")
    InstallManager.install(FlaskSQLAlchemyInstaller)
    click.echo("Done")


install.add_command(sqlalchemy)


@click.command(help="Install Flask-SQLAlchemy")
def migrate():
    click.echo("Installing Flask-Migrate")
    InstallManager.install(FlaskMigrateInstaller)
    click.echo("Done")


install.add_command(migrate)


@click.command(help="Install Flask-WTF")
def wtf():
    click.echo("Installing Flask-WTF")
    InstallManager.install(FlaskWTFInstaller)
    click.echo("Done")


install.add_command(wtf)


@click.command(help="Install Flask-Login")
def login():
    click.echo("Installing Flask-Login")
    InstallManager.install(FlaskLoginInstaller)
    click.echo("Done")
    click.echo("Additional configuration steps required:")
    click.echo(f'{TAB}1. Complete "load_user()" function in src/__init__.py')


install.add_command(login)


@click.command(help="Install Flask-Mail")
def mail():
    click.echo("Installing Flask-Mail")
    InstallManager.install(FlaskMailInstaller)
    click.echo("Done")
    click.echo("Additional configuration steps required:")
    click.echo(f"{TAB}1. Set Flask-Mail config variables in src/config.py")


install.add_command(mail)


@click.command(help="Install Flask-Talisman")
def talisman():
    click.echo("Installing Flask-Talisman")
    InstallManager.install(FlaskTalismanInstaller)
    click.echo("Done")
    click.echo("Additional configuration steps recommended:")
    click.echo(
        f"{TAB}1. Set content security policy (CSP) as documented here: "
        "https://github.com/GoogleCloudPlatform/flask-talisman#content-security-policy"
    )


install.add_command(talisman)

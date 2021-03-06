import click
import os
from ..generators import *
from flask.cli import with_appcontext
from flask import current_app
from ..installers import FlaskSQLAlchemyInstaller


@click.group(help="Commands for generating files")
def generate():
    pass


@click.command(help="Generate a new route")
@click.argument("name")
@click.argument("url_rules", default=None, nargs=-1)
def route(name, url_rules):
    click.echo(f"Generating route: {name}")
    for checkpoint in RouteGenerator.generate(name, url_rules):
        click.secho(checkpoint, fg="green")
    click.echo("Done")


generate.add_command(route)


@click.command(help="Generate a new stylesheet")
@click.argument("name")
def stylesheet(name):
    click.echo(f"Generating stylesheet: {name}")
    for checkpoint in StylesheetGenerator.generate(name):
        click.secho(checkpoint, fg="green")
    click.echo("Done")


generate.add_command(stylesheet)


@click.command(help="Generate a new db model")
@click.argument("name")
def model(name):
    click.echo(f"Generating model: {name}")
    for checkpoint in ModelGenerator.generate(name):
        click.secho(checkpoint, fg="green")
    click.echo("Done")


generate.add_command(model)

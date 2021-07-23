import click
import os
from ..generators import RouteGenerator, StylesheetGenerator
from flask.cli import with_appcontext


@click.group(help="Commands for generating files")
def generate():
    pass


@click.command(help="Generate a new route")
@click.argument("name")
def route(name):
    click.echo(f"Generating route: {name}")
    for checkpoint in RouteGenerator.generate(name):
        click.secho(checkpoint, fg="green")
    click.echo("Done")


generate.add_command(route)


@click.command(help="Generate a new stylesheet")
@click.argument("name")
@with_appcontext
def stylesheet(name):
    click.echo(f"Generating stylesheet: {name}")
    for checkpoint in StylesheetGenerator.generate(name):
        click.secho(checkpoint, fg="green")
    click.echo("Done")


generate.add_command(stylesheet)

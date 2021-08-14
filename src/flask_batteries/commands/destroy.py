import click
import os
from ..generators import *
from flask.cli import with_appcontext


@click.group(help="Commands for destroying files")
def destroy():
    pass


@click.command(help="Destroy a route")
@click.argument("name")
def route(name):
    click.echo(f"Destroying route: {name}")
    for checkpoint in RouteGenerator.destroy(name):
        click.secho(checkpoint, fg="red")
    click.echo("Done")


destroy.add_command(route)


@click.command(help="Destroy a stylesheet")
@click.argument("name")
@with_appcontext
def stylesheet(name):
    click.echo(f"Destroying stylesheet: {name}")
    for checkpoint in StylesheetGenerator.destroy(name):
        click.secho(checkpoint, fg="red")
    click.echo("Done")


destroy.add_command(stylesheet)


@click.command(help="Destroy a model")
@click.argument("name")
def model(name):
    click.echo(f"Destroying model: {name}")
    for checkpoint in ModelGenerator.destroy(name):
        click.secho(checkpoint, fg="red")
    click.echo("Done")


destroy.add_command(model)

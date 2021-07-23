import click
import os
from ..generators import RouteGenerator


@click.group(help="Commands for generating files")
def generate():
    pass


@click.command(help="Generate a new route")
@click.argument("name")
def route(name):
    click.echo(f"Generating route: {name}")
    RouteGenerator.generate(name)
    click.echo("Done")


generate.add_command(route)

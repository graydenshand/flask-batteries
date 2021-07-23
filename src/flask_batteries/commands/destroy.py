import click
import os
from ..helpers import snake_to_camel_case
from ..generators import RouteGenerator


@click.group(help="Commands for destroying files")
def destroy():
    pass


@click.command(help="Destroy a route")
@click.argument("name")
def route(name):
    click.echo(f"Destroying route: {name}")
    RouteGenerator.destroy(name)
    click.echo("Done")


destroy.add_command(route)

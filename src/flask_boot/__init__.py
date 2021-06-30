import click


@click.group()
def cli():
    pass


# Register commands
from .new import new
cli.add_command(new)
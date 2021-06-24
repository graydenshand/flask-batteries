import click

@click.group()
def cli():
	pass

# Register commands
from .new import new
cli.add_command(new)

from .destroy import destroy
cli.add_command(destroy)
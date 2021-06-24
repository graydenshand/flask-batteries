#!/opt/homebrew/bin/python3
import os
import sys
import shutil
import click

@click.command()
@click.argument("name")
def destroy(name):
	print("Destroying app named: %s" % name)
	shutil.rmtree(name)
import click
import subprocess


@click.command(help="Start Webpack dev server")
def watch():
    subprocess.run("npx webpack serve", shell=True)

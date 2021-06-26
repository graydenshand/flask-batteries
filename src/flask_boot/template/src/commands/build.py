import subprocess
import click

@click.command(help="Build static assets")
@click.option("--bail/--no-bail", default=False, help="Exit with error if build fails")
def build(bail):
  print("CALLING FLASK BUILD")
  if bail:
    proc = subprocess.run("npx webpack --bail", shell=True)
    if proc.returncode != 0:
      exit(1)
  else:
    subprocess.run("npx webpack", shell=True)

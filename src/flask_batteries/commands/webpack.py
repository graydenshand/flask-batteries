import click
import subprocess


@click.group(help="Webpack asset pipeline")
def webpack():
    pass


@click.command(help="Compile static assets with Webpack")
@click.option("--bail/--no-bail", default=False, help="Exit with error if build fails")
def build(bail):
    """
    Compile static assets with Webpack

    If --bail is passed, exit with an error code if compilation fails.
    This is useful for CI tests.
    """
    if bail:
        proc = subprocess.run(["npx", "webpack", "--bail"])
        if proc.returncode != 0:
            exit(1)
    else:
        subprocess.run(["npx", "webpack"])


webpack.add_command(build)


@click.command(help="Start Webpack dev server")
def watch():
    """
    Compile static assets with Webpack (in development mode), and watch for changes.

    Compiles faster than the `build` command.
    """
    subprocess.run(["npx", "webpack", "serve"])


webpack.add_command(watch)

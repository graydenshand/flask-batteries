import click
import os
from .generate import snake_to_camel_case


@click.group(help="Commands for destroying files")
def destroy():
    pass


@click.command(help="Destroy a route")
@click.argument("name")
def route(name):
    click.echo(f"Destroying route: {name}")
    name = name.lower()
    # Destroy route file: routes/<name>.py
    os.remove(f"src/routes/{name}.py")
    click.secho(f"Removed file src/routes/{name}.py", fg="red")
    # Destroy template: templates/<name>.html
    os.remove(f"src/templates/{name}.html")
    click.secho(f"Removed file src/templates/{name}.html", fg="red")
    # Destroy test: routes/<name>.py
    os.remove(f"test/routes/test_{name}.py")
    click.secho(f"Removed file test/routes/test_{name}.py", fg="red")
    # Update routes/__init__.py
    with open("src/routes/__init__.py", "r+") as f:
        content = f.read()
        content = content.split("\n")
        content.remove(f"from .{name} import {name}_view")
        content.remove(
            f"\tapp.add_url_rule(\"/{name.replace('_','-')}/\", view_func={name}_view)"
        )
        f.seek(0)
        f.write("\n".join(content))
        f.truncate()
    click.secho(f"Updated file src/routes/__init__.py", fg="red")
    click.echo("Done")


destroy.add_command(route)

import click
import os


@click.group(help="Commands for generating files")
def generate():
    pass


route_template = """from flask import render_template
from flask.views import MethodView


class {camel_name}(MethodView):
    def get(self):
        return render_template("{name}.html")

{name}_view = {camel_name}.as_view("{name}")"""

view_template = """{{% extends 'base.html' %}}

{{% block body %}}
<h1>{camel_name}</h1>
<p>Edit <b><i>src/templates/{name}.html</i></b> to make changes to this page.</p>
{{% endblock %}}
"""

test_template = """from ..fixtures import client, app


def test_{name}_returns_ok_response(client):
    r = client.get("/{url_name}", follow_redirects=True)
    assert r.status == "200 OK"
"""


def snake_to_camel_case(string):
    return "".join([seg[0].upper() + seg[1:] for seg in string.split("_")])


@click.command(help="Generate a new route")
@click.argument("name")
def route(name):
    click.echo(f"Generating route: {name}")
    name = name.lower()
    template_data = {
        "camel_name": snake_to_camel_case(name),
        "name": name,
        "url_name": name.replace("_", "-"),
    }
    # Generate route file: routes/<name>.py
    with open(f"src/routes/{name}.py", "w") as f:
        content = route_template.format(**template_data)
        f.write(content)
    click.secho(f"Created file src/routes/{name}.py", fg="green")
    # Generate template: templates/<name>.html
    with open(f"src/templates/{name}.html", "w") as f:
        content = view_template.format(**template_data)
        f.write(content)
    click.secho(f"Created file src/templates/{name}.html", fg="green")
    # Generate test: routes/<name>.py
    with open(f"test/routes/test_{name}.py", "w") as f:
        content = test_template.format(**template_data)
        f.write(content)
    click.secho(f"Created file test/routes/test_{name}.py", fg="green")
    # Update src/routes/__init__.py
    with open("src/routes/__init__.py", "r+") as f:
        content = f.read()
        content = content.split("\n")
        i = 0
        while i < len(content):
            line = content[i]
            if line == "" or line == "def register_routes(app):":
                content.insert(i, f"from .{name} import {name}_view")
                break
            i += 1
        content.append(
            f"\tapp.add_url_rule(\"/{name.replace('_','-')}/\", view_func={name}_view)"
        )
        f.seek(0)
        f.write("\n".join(content))
        f.truncate()
    click.secho(f"Updated file src/routes/__init__.py", fg="green")
    click.echo("Done")


generate.add_command(route)

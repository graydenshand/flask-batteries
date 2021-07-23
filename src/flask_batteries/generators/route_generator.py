from .base_generator import BaseGenerator
from ..helpers import snake_to_camel_case, create_file
from ..config import TAB
import os


class RouteGenerator(BaseGenerator):
    @staticmethod
    def generate(name):
        name = name.lower()
        template_data = {
            "camel_name": snake_to_camel_case(name),
            "name": name,
            "url_name": name.replace("_", "-"),
        }
        # Generate route file: routes/<name>.py
        content = route_template.format(**template_data)
        create_file(os.path.join("src", "routes", f"{name}.py"), content)

        # Generate template: templates/<name>.html
        content = view_template.format(**template_data)
        create_file(os.path.join("src", "templates", f"{name}.html"), content)

        # Generate test: routes/<name>.py
        content = test_template.format(**template_data)
        create_file(os.path.join("test", "routes", f"test_{name}.py"), content)

        # Update src/routes/__init__.py
        with open("src/routes/__init__.py", "r+") as f:
            content = f.read()
            content = content.split("\n")
            i = 0
            while i < len(content):
                line = content[i]
                if line == "" or line == "def register_routes(app):":
                    # Import view from route file
                    content.insert(i, f"from .{name} import {name}_view")
                    break
                i += 1
            content.append(
                # Add url rule
                f"{TAB}app.add_url_rule(\"/{name.replace('_','-')}/\", view_func={name}_view)"
            )
            f.seek(0)
            f.write("\n".join(content))
            f.truncate()

    @staticmethod
    def destroy(name):
        name = name.lower()
        # Destroy route file: routes/<name>.py
        os.remove(f"src/routes/{name}.py")
        # Destroy template: templates/<name>.html
        os.remove(f"src/templates/{name}.html")
        # Destroy test: routes/<name>.py
        os.remove(f"test/routes/test_{name}.py")
        # Update routes/__init__.py
        with open("src/routes/__init__.py", "r+") as f:
            content = f.read()
            content = content.split("\n")
            content.remove(f"from .{name} import {name}_view")
            content.remove(
                f"{TAB}app.add_url_rule(\"/{name.replace('_','-')}/\", view_func={name}_view)"
            )
            f.seek(0)
            f.write("\n".join(content))
            f.truncate()


# Template for generated file in src/routes
route_template = """from flask import render_template
from flask.views import MethodView


class {camel_name}(MethodView):
    def get(self):
        return render_template("{name}.html")

{name}_view = {camel_name}.as_view("{name}")"""

# Template for generated file in src/templates
view_template = """{{% extends 'base.html' %}}

{{% block body %}}
<h1>{camel_name}</h1>
<p>Edit <b><i>src/templates/{name}.html</i></b> to make changes to this page.</p>
{{% endblock %}}
"""

# Template for generated file in test/routes
test_template = """from ..fixtures import client, app


def test_{name}_returns_ok_response(client):
    r = client.get("/{url_name}", follow_redirects=True)
    assert r.status == "200 OK"
"""

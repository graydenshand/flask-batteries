from .base_generator import BaseGenerator
from ..helpers import snake_to_pascal_case, create_file
from ..config import TAB
import os
import re


class RouteGenerator(BaseGenerator):
    @staticmethod
    def generate(name, url_rules=[]):
        name = name.lower()
        template_data = {
            "pascal_name": snake_to_pascal_case(name),
            "name": name,
            "url_name": name.replace("_", "-"),
        }
        # Generate route file: routes/<name>.py
        content = route_template.format(**template_data)
        create_file(os.path.join("src", "routes", f"{name}.py"), content)
        yield f'Created {os.path.join("src", "routes", f"{name}.py")}'

        # Generate template: templates/<name>.html
        content = view_template.format(**template_data)
        create_file(os.path.join("src", "templates", f"{name}.html"), content)
        yield f'Created {os.path.join("src", "templates", f"{name}.html")}'

        # Generate test: routes/<name>.py
        content = test_template.format(**template_data)
        create_file(os.path.join("test", "routes", f"test_{name}.py"), content)
        yield f'Created {os.path.join("test", "routes", f"test_{name}.py")}'

        # Update src/routes/__init__.py
        with open(os.path.join("src", "routes", "__init__.py"), "r+") as f:
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
            if url_rules:
                for rule in url_rules:
                    # Remove trailing slash if passed
                    rule = rule.rstrip("/")
                    # Add url rule (with trailing slash)
                    content.append(
                        f'{TAB}app.add_url_rule("{rule}/", view_func={name}_view)'
                    )
            else:
                content.append(
                    # Add url rule
                    f"{TAB}app.add_url_rule(\"/{name.replace('_','-')}/\", view_func={name}_view)"
                )
            f.seek(0)
            f.write("\n".join(content))
            f.truncate()
        yield f'Added url_rule(s) to {os.path.join("src", "routes", "__init__.py")}'

    @staticmethod
    def destroy(name):
        name = name.lower()
        # Destroy route file: routes/<name>.py
        os.remove(os.path.join("src", "routes", f"{name}.py"))
        yield f'Destroyed {os.path.join("src", "routes", f"{name}.py")}'
        # Destroy template: templates/<name>.html
        os.remove(os.path.join("src", "templates", f"{name}.html"))
        yield f'Destroyed {os.path.join("src", "templates", f"{name}.html")}'
        # Destroy test: routes/<name>.py
        os.remove(os.path.join("test", "routes", f"test_{name}.py"))
        yield f'Destoryed {os.path.join("test", "routes", f"test_{name}.py")}'
        # Update routes/__init__.py
        with open(os.path.join("src", "routes", "__init__.py"), "r+") as f:
            content = f.read()
            pattern = fr"from .{name} import {name}_view\n"
            content = re.sub(pattern, "", content)
            pattern = fr'{TAB}app.add_url_rule\(".*?", view_func={name}_view\)\n'
            content = re.sub(pattern, "", content)
            f.seek(0)
            f.truncate()
            f.write(content)
        yield f'Removed URL rule(s) from {os.path.join("src", "routes", "__init__.py")}'


# Template for generated file in src/routes
route_template = """from flask import render_template
from flask.views import MethodView


class {pascal_name}(MethodView):
    def get(self):
        return render_template("{name}.html")

{name}_view = {pascal_name}.as_view("{name}")"""

# Template for generated file in src/templates
view_template = """{{% extends 'base.html' %}}

{{% block body %}}
<h1>{pascal_name}</h1>
<p>Edit <b><i>src/templates/{name}.html</i></b> to make changes to this page.</p>
{{% endblock %}}
"""

# Template for generated file in test/routes
test_template = """from ..fixtures import client, app


def test_{name}_returns_ok_response(client):
    r = client.get("/{url_name}", follow_redirects=True)
    assert r.status == "200 OK"
"""

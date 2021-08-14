from .base_generator import BaseGenerator
from ..installers import FlaskMarshmallowInstaller, FlaskSQLAlchemyInstaller
from ..helpers import snake_to_pascal_case, create_file, add_to_init, remove_from_file
import re
import os
from ..config import TAB


class ModelGenerator(BaseGenerator):
    @staticmethod
    def generate(name):
        """
        Generate a new SQLAlchemy model
        """
        if not FlaskSQLAlchemyInstaller.verify():
            raise RuntimeError(
                "Cannot generate model, Flask-SQLAlchemy is not installed"
            )

        pascal_name = snake_to_pascal_case(name)
        template_data = {"pascal_name": pascal_name, "name": name}

        # Create src/models/{name}.py
        if FlaskMarshmallowInstaller.verify():
            content = model_template_w_schema.format(**template_data)
        else:
            content = model_template.format(**template_data)
        create_file(os.path.join("src", "models", f"{name}.py"), content)
        yield f"Created {os.path.join('src', 'models', f'{name}.py')}"

        # Create test/models/test_{name}.py
        test_content = test_file_template.format(**template_data)
        create_file(os.path.join("test", "models", f"test_{name}.py"), test_content)
        yield f"Created {os.path.join('test', 'models', f'test_{name}.py')}"

        # Import model into src/models/__init__.py
        with open(os.path.join("src", "models", "__init__.py"), "a") as f:
            f.write(f"from .{name} import {pascal_name}\n")

        yield f"Updated {os.path.join('src', 'models', '__init__.py')}"

        # Import model into src/__init__.py
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            content = f.read()

            pattern = r"(from src\.models import .*)\n"
            if re.search(pattern, content):
                content = re.sub(pattern, rf"\g<1>, {pascal_name}\n", content)
            else:
                # first model
                lines = content.split("\n")
                index = lines.index(f"{TAB}{TAB}Batteries(app)")
                lines_to_insert = [
                    f"{TAB}{TAB}# Import models",
                    f"{TAB}{TAB}from src.models import {pascal_name}",
                    "",  # blank line for spacing
                ]
                lines = lines[:index] + lines_to_insert + lines[index:]
                content = "\n".join(lines)

            f.seek(0)
            f.truncate()
            f.write(content)

        # Inject model into shell context
        add_to_init(shell_vars=[f'"{pascal_name}": {pascal_name},'])

        yield f"Updated {os.path.join('src', '__init__.py')}"

    @staticmethod
    def destroy(name):
        """
        Destroy a SQLAlchemy model
        """
        if not FlaskSQLAlchemyInstaller.verify():
            raise RuntimeError(
                "Cannot destroy model, Flask-SQLAlchemy is not installed"
            )

        pascal_name = snake_to_pascal_case(name)

        # Delete the model file at src/models/{name}.py
        os.remove(os.path.join("src", "models", f"{name}.py"))

        yield f"Destroyed {os.path.join('src', 'models', f'{name}.py')}"

        # Delete the test fiel at test/models/test_{name}.py
        os.remove(os.path.join("test", "models", f"test_{name}.py"))
        yield f"Destroyed {os.path.join('test', 'models', f'test_{name}.py')}"

        # Remove import from src/models/__init__.py
        with open(os.path.join("src", "models", "__init__.py"), "r+") as f:
            content = f.read()
            pattern = fr"from .{name} import {pascal_name}\n"
            content = re.sub(pattern, "", content)
            f.seek(0)
            f.truncate()
            f.write(content)

        yield f"Updated {os.path.join('src', 'models', '__init__.py')}"

        # Remove import from src/__init__.py
        with open(os.path.join("src", "__init__.py"), "r+") as f:
            content = f.read()
            pattern = fr"from src\.models import {pascal_name}\n"
            if re.search(pattern, content):
                lines_to_remove = [
                    "# Import models",
                    "from src.models import ",
                    f'"{pascal_name}": {pascal_name},',
                ]
            else:
                pattern = fr"(from src\.models import .*)({pascal_name},? ?)(.*)\n"
                content = re.sub(pattern, r"\g<1>\g<3>\n", content)

                # Check for trailing comma (if deleted last model in list)
                pattern = r"(from src\.models import .*)(, ?)\n"
                content = re.sub(pattern, r"\g<1>\n", content)
                f.seek(0)
                f.truncate()
                f.write(content)
                lines_to_remove = [f'"{pascal_name}": {pascal_name},']

        # Remove lines
        remove_from_file(os.path.join("src", "__init__.py"), lines_to_remove)

        yield f"Updated {os.path.join('src', '__init__.py')}"


model_template = """from src import db

class {pascal_name}(db.Model):
	__tablename__ = "{name}"
	id = db.Column(db.Integer, primary_key=True)
"""


model_template_w_schema = """from src import db, ma

class {pascal_name}Model(db.Model):
	__tablename__ = "{name}"
	id = db.Column(db.Integer, primary_key=True)

class {pascal_name}Schema(ma.Schema):
	class Meta:
		model = {pascal_name}Model
		include_fk = True
		include_relationships = False


class {pascal_name}({pascal_name}Model):
		schema = {pascal_name}Schema
"""


test_file_template = """from src.models import {pascal_name}

def test_init_{name}():
	# Test that {pascal_name} instantiates without error
	{name} = {pascal_name}()
"""

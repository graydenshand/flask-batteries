from ..conf_tests import app, cli
from flask_batteries.commands import generate, destroy, new
import os
import traceback
from flask_batteries.config import TAB
from flask_batteries.helpers import verify_file
from flask_batteries.installers import FlaskSQLAlchemyInstaller
import subprocess


def test_model_generator(app, cli):
    result = cli.invoke(generate, ["model", "user"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    result = cli.invoke(generate, ["model", "user_posts"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    assert os.path.exists(os.path.join("src", "models", "user.py"))
    assert os.path.exists(os.path.join("test", "models", "test_user.py"))
    assert os.path.exists(os.path.join("src", "models", "user_posts.py"))
    assert os.path.exists(os.path.join("test", "models", "test_user_posts.py"))

    # Verify models/__init__.py
    lines_to_verify = [
        "from .user import User",
        "from .user_posts import UserPosts",
    ]
    assert verify_file(os.path.join("src", "models", "__init__.py"), lines_to_verify)

    # Verify src/__init__.py
    lines_to_verify = [
        "# Import models",
        "from src.models import User, UserPosts",
    ]
    assert verify_file(os.path.join("src", "__init__.py"), lines_to_verify)

    # Destroy "user_posts" model
    result = cli.invoke(destroy, ["model", "user_posts"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Verify src/__init__.py
    lines_to_verify = [
        "# Import models",
        "from src.models import User",
    ]
    assert verify_file(os.path.join("src", "__init__.py"), lines_to_verify)

    # Destroy "user" model
    result = cli.invoke(destroy, ["model", "user"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Verify src/__init__.py
    lines_to_verify = [
        "# Import models",
        "from src.models import User",
    ]
    assert not verify_file(os.path.join("src", "__init__.py"), lines_to_verify)

    assert not os.path.exists(os.path.join("src", "models", "user.py"))
    assert not os.path.exists(os.path.join("test", "models", "test_user.py"))
    assert not os.path.exists(os.path.join("src", "models", "user_posts.py"))
    assert not os.path.exists(os.path.join("test", "models", "test_user_posts.py"))


def test_fails_when_sqlalchemy_not_installed(cli):
    result = cli.invoke(new, ["app", "--skip-db"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    result = cli.invoke(generate, ["model", "user"])
    assert result.exit_code != 0

    result = cli.invoke(destroy, ["model", "user"])
    assert result.exit_code != 0


def test_generated_test_passes(cli, app):
    result = cli.invoke(generate, ["model", "user"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

    # Run the generated app's test suite and verify exit code is 0
    if os.name != "nt":
        run_tests = subprocess.run(
            "source venv/bin/activate && pytest -k test_user", shell=True
        )
    else:
        run_tests = subprocess.run(
            "venv\\Scripts\\activate && pytest -k test_user", shell=True
        )
    assert run_tests.returncode == 0, run_tests.stdout

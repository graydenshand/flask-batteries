from ..conf_tests import app, cli
from flask_batteries.commands import generate, destroy
import os
import traceback
from flask_batteries.config import TAB


def test_route_generator(cli, app):
    # Generate files
    result = cli.invoke(generate, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" in content
        assert f'{TAB}app.add_url_rule("/sign-up/", view_func=sign_up_view)' in content

    # Destroy generated files
    result = cli.invoke(destroy, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert not os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert not os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert not os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" not in content
        assert '\tapp.add_url_rule("/sign-up/", view_func=sign_up_view)' not in content


def test_route_generator_with_multiple_url_rules(cli, app):
    # Generate files
    result = cli.invoke(generate, ["route", "sign_up", "/sign-up", "/register"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" in content
        assert f'{TAB}app.add_url_rule("/sign-up/", view_func=sign_up_view)' in content
        assert f'{TAB}app.add_url_rule("/register/", view_func=sign_up_view)' in content

    # Destroy generated files
    result = cli.invoke(destroy, ["route", "sign_up"])
    assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
    assert not os.path.exists(os.path.join("src", "routes", "sign_up.py"))
    assert not os.path.exists(os.path.join("src", "templates", "sign_up.html"))
    assert not os.path.exists(os.path.join("test", "routes", "test_sign_up.py"))
    with open(os.path.join("src", "routes", "__init__.py"), "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" not in content
        assert '\tapp.add_url_rule("/sign-up/", view_func=sign_up_view)' not in content
        assert '\tapp.add_url_rule("/register/", view_func=sign_up_view)' not in content

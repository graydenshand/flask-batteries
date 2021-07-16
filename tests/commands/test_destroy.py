from ..conf_tests import app, route, cli
from flask_batteries.commands import destroy
import os


def test_destroy_route_destroys_correct_files(cli, route, app):
    cli.invoke(destroy, ["route", "sign_up"])
    assert not os.path.exists("src/routes/sign_up.py")
    assert not os.path.exists("src/templates/sign_up.html")
    assert not os.path.exists("test/routes/test_sign_up.py")
    with open("src/routes/__init__.py", "r") as f:
        content = f.read()
        assert "from .sign_up import SignUp" not in content
        assert (
            '\tapp.add_url_rule("/sign-up/", view_func=SignUp.as_view("sign_up"))'
            not in content
        )

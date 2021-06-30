from ..fixtures import client, app, cli
from src.commands import generate
import os

def test_generate_route_creates_correct_files(cli):
    cli.invoke(generate, ['route', 'sign_up'])
    assert os.path.exists("src/routes/sign_up.py")
    assert os.path.exists("src/templates/sign_up.html")
    assert os.path.exists("test/routes/test_sign_up.py")
    with open("src/routes/__init__.py", "r") as f:
        content = f.read()
        assert "from .sign_up import sign_up_view" in content
        assert "\tapp.add_url_rule(\"/sign-up/\", view_func=sign_up_view)" in content


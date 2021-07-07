from ..fixtures import client, app
from src.helpers import static_url_for


def test_static_url_for_returns_correct_url(client, app):
    app.config["SERVER_NAME"] = "127.0.0.1:5000"
    assert app.config["USE_WEBPACK_DEV_SERVER"] == False
    with app.test_request_context():
        assert static_url_for("test.txt") == f"/static/test.txt"
        app.config["USE_WEBPACK_DEV_SERVER"] = True
        assert static_url_for("test.txt") == f"http://localhost:3000/static/test.txt"

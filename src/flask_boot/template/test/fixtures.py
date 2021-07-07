import pytest
from src import create_app
from src.config import TestingConfig
from click.testing import CliRunner


@pytest.fixture
def app():
    # Create a new application instance
    app = create_app(TestingConfig)

    with app.app_context():
        # Run the test
        yield app


@pytest.fixture
def client(app):
    return app.test_client()

import pytest
from api.app import create_app

pytest.OAUTH_TOKEN = ''
pytest.BASE_API = ''


@pytest.fixture
def app():
    """Get the application to test
    """
    app = create_app()
    pytest.BASE_API = app.config['API_PREFIX_URL']
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
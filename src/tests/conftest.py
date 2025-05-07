import pytest
from starlette.testclient import TestClient

from app.main import app

@pytest.fixture(scope="module")
def test_app():
    """
    Create a test client for the FastAPI app.
    """
    with TestClient(app) as client:
        yield client

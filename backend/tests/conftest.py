import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """
    Fixture to provide a TestClient for the FastAPI app.

    Returns:
        TestClient: A TestClient instance for the FastAPI app.
    """
    return TestClient(app)

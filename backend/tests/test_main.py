import pytest
from main import app
from httpx import AsyncClient

def test_app_metadata():
    """
    GIVEN: FastAPI app instance
    WHEN: Retrieving app metadata
    THEN: The app metadata should match the expected values
    """

    assert app.title == "English AI Tutor API"
    assert app.version == "0.1.0"


@pytest.mark.asyncio
async def test_docs_available(client: AsyncClient):
    """
    GIVEN: FastAPI app instance
    WHEN: Accessing the /docs endpoint
    THEN: The response status code should be 200 (OK)
    """

    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_redoc_available(client: AsyncClient):
    """
    GIVEN: FastAPI app instance
    WHEN: Accessing the /redoc endpoint
    THEN: The response status code should be 200 (OK)
    """
    response = await client.get("/redoc")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_cors_headers(client: AsyncClient):
    """
    GIVEN: FastAPI app instance
    WHEN: Sending an OPTIONS request with CORS headers
    THEN: The response should include the appropriate CORS headers"""
    origin = "http://example.com"

    response = await client.options(
        "/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == origin


@pytest.mark.asyncio
async def test_lifespan_shutdown_disposes_engine(monkeypatch):
    """
    GIVEN: FastAPI app instance with a lifespan event
    WHEN: The app is started and then shut down
    THEN: The SQLAlchemy engine's dispose method should be called
    """
    disposed = False

    async def mock_dispose(self):
        nonlocal disposed
        disposed = True

    from sqlalchemy.ext.asyncio import AsyncEngine
    monkeypatch.setattr(AsyncEngine, "dispose", mock_dispose)

    from asgi_lifespan import LifespanManager

    async with LifespanManager(app):
        pass

    assert disposed is True

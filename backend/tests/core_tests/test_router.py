import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """
    GIVEN: FastAPI app instance with a health check endpoint
    WHEN: Accessing the /healthcheck endpoint
    THEN: The response status code should be 200 (OK) and the response body should indicate that the
    application is healthy
    """
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_health_check_failure(client: AsyncClient, monkeypatch):
    """
    GIVEN: FastAPI app instance where healthcheck service fails
    WHEN: Accessing the /healthcheck endpoint
    THEN: The response status code should be 503 and indicate database unavailability
    """

    async def mock_perform_healthcheck(_):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

    monkeypatch.setattr("core.router.perform_healthcheck", mock_perform_healthcheck)

    response = await client.get("/healthcheck")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}

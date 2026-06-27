from fastapi.testclient import TestClient
from fastapi import HTTPException, status


def test_health_check(client: TestClient):
    """
    GIVEN: FastAPI app instance with a health check endpoint
    WHEN: Accessing the /healthcheck endpoint
    THEN: The response status code should be 200 (OK) and the response body should indicate that the application is healthy
    """
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_failure(client: TestClient, monkeypatch):
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

    # Patch the function where it is USED (important!)
    monkeypatch.setattr(
        "core.services.healthcheck_service.perform_healthcheck",
        mock_perform_healthcheck
    )

    response = client.get("/healthcheck")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}

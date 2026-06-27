import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.healthcheck_service import perform_healthcheck


@pytest.mark.asyncio
async def test_perform_healthcheck_success():
    """
    GIVEN: A mock AsyncSession
    WHEN: The perform_healthcheck function is called
    THEN: It should return a dictionary indicating the health status of the application
    """
    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=None)

    result = await perform_healthcheck(mock_session)

    mock_session.execute.assert_called_once()
    assert result == {"status": "healthy"}


@pytest.mark.asyncio
async def test_perform_healthcheck_failure():
    """
    GIVEN: A mock AsyncSession that raises an exception
    WHEN: The perform_healthcheck function is called
    THEN: It should raise an HTTPException with a 503 status code and the appropriate detail message
    """
    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(side_effect=Exception("DB error"))

    with pytest.raises(HTTPException) as exc_info:
        await perform_healthcheck(mock_session)

    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exc_info.value.detail == "Database unavailable"

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.services.healthcheck_service import perform_healthcheck


router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    """
    Health check endpoint to verify the database connection.

    Args:
        db (AsyncSession): The database session to use for the health check.

    Returns:
        dict: A dictionary indicating the health status of the application.
    """
    await perform_healthcheck(db)
    return {"status": "healthy"}

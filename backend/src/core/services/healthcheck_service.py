
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def perform_healthcheck(db: AsyncSession) -> bool:
    """
    Perform a health check on the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        bool: True if the health check is successful, False otherwise.
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc
    return {"status": "healthy"}
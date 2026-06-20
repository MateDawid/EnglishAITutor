from typing import Annotated

from auth.models import DbUser
from auth.services.token_service import oauth2_scheme, verify_access_token
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

def get_user_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """Extract the user ID from the JWT access token."""
    user_id = verify_access_token(token)
    if user_id is None:
        raise InvalidTokenException()
    try:
        return int(user_id)
    except (TypeError, ValueError):
        raise InvalidTokenException()

def get_db_user_by_id(user_id: int, db: AsyncSession) -> DbUser:
    """Fetch the user from the database by ID."""
    result = db.execute(select(DbUser).where(DbUser.id == user_id))
    db_user = result.scalars().first()
    if db_user is None:
        raise UserNotFoundException()
    return db_user

async def get_current_user_from_db(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DbUser:
    """Get the current user from the database based on the JWT access token."""
    user_id = get_user_id_from_token(token)
    return get_db_user_by_id(user_id, db)

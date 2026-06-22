from typing import Annotated
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.models import DbUser
from auth.services.token_service import oauth2_scheme, verify_access_token
from auth.services.user_services.exceptions import InvalidTokenException, UserNotFoundException


def get_user_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> uuid.UUID:
    """
    Extract the user ID from the JWT access token.
    
    Args:
        token (str): The JWT access token provided by the client.
    
    Returns:
        uuid.UUID: The user ID extracted from the token.
    """
    user_id = verify_access_token(token)
    if user_id is None:
        raise InvalidTokenException()
    try:
        return uuid.UUID(user_id)
    except (TypeError, ValueError):
        raise InvalidTokenException()


async def get_db_user_by_id(user_id: uuid.UUID, db: AsyncSession) -> DbUser:
    """
    Fetch the user from the database by ID.
    
    Args:
        user_id (uuid.UUID): The ID of the user to fetch.
        db (AsyncSession): The database session to use for the query.
    
    Returns:
        DbUser: The user object corresponding to the given ID.
    """
    result = await db.execute(select(DbUser).where(DbUser.id == user_id))
    db_user = result.scalars().first()
    if db_user is None:
        raise UserNotFoundException()
    return db_user


async def get_current_user_from_db(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]) -> DbUser:
    """
    Get the current user from the database based on the JWT access token.

    Args:
        token (str): The JWT access token provided by the client.
        db (AsyncSession): The database session to use for the query.

    Returns:
        DbUser: The user object corresponding to the current user.
    """
    user_id = get_user_id_from_token(token)
    return await get_db_user_by_id(user_id, db)

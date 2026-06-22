from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.schemas import TokenSchema
from auth.models import DbUser
from auth.services.token_service import create_access_token, verify_password
from auth.services.user_services.exceptions import InvalidCredentialsException


async def get_user_from_db_by_email(email: str, db: Annotated[AsyncSession, Depends(get_db)]) -> DbUser:
    """
    Fetch the user from the database by email (case-insensitive).

    Args:
        email (str): The email address of the user to fetch.
        db (AsyncSession): The database session to use for the query.

    Returns:
        DbUser: The user object corresponding to the given email.
    """
    result = await db.execute(
        select(DbUser).where(
            func.lower(DbUser.email) == email.lower(),
        ),
    )
    return result.scalars().first()


async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]) -> TokenSchema:
    """
    Authenticate the user and return an access token.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username (email) and password.
        db (AsyncSession): The database session to use for the query.
    
    Returns:
        TokenSchema: The access token and token type if authentication is successful.
    """
    user = await get_user_from_db_by_email(form_data.username, db)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise InvalidCredentialsException()

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenSchema(access_token=access_token, token_type="bearer")

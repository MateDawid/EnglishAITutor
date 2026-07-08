from typing import Annotated

from auth.services.token_service import hash_password
from auth.services.exceptions import PasswordMismatchException, UserAlreadyExistsException
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.schemas import UserCreateSchema
from auth.models import DbUser


async def validate_user_email_uniqueness(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Validate that the provided email is unique in the database.

    Args:
        email (str): The email address to validate.
        db (AsyncSession): The database session to use for the query.

    Raises:
        UserAlreadyExistsException: If a user with the provided email already exists.
    """
    result = await db.execute(
        select(DbUser).where(func.lower(DbUser.email) == email.lower()),
    )
    existing_email = result.scalars().first()
    if existing_email:
        raise UserAlreadyExistsException()


def validate_user_passwords(password_1: str, password_2: str):
    """
    Validate that the provided passwords match.

    Args:
        password_1 (str): The first password.
        password_2 (str): The second password.

    Raises:
        PasswordMismatchException: If the passwords do not match.
    """
    if password_1 != password_2:
        raise PasswordMismatchException()


async def save_user_in_db(user: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> DbUser:
    """
    Create a new user in the database.

    Args:
        user (UserCreateSchema): The user data to create.
        db (AsyncSession): The database session to use for the operation.

    Returns:
        DbUser: The newly created user object.
    """
    user = DbUser(
        email=user.email.lower(),
        password_hash=hash_password(user.password_1),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def register_user(form: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> DbUser:
    """
    Register a new user in the database.
    
    Args:
        form (UserCreateSchema): The user data to register.
        db (AsyncSession): The database session to use for the operation.

    Returns:
        DbUser: The newly registered user.
    """
    await validate_user_email_uniqueness(form.email, db)
    validate_user_passwords(form.password_1, form.password_2)
    return await save_user_in_db(form, db)

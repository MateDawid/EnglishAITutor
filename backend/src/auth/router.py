from datetime import UTC, datetime, timedelta
from typing import Annotated

from auth.services.user_services.current_user_service import get_current_user_from_db
from auth.services.user_services.register_user_service import register_user_in_db
from auth.services.token_service import hash_password, verify_password, create_access_token
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from auth.schemas import TokenSchema, UserCreateSchema, UserRetrieveSchema
from auth.models import DbUser


router = APIRouter()


@router.post("/register", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def register_user(form: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> UserRetrieveSchema:
    """
    View to register a new user in the database.

    Args:
        form (UserCreateSchema): The user data to register.
        db (AsyncSession): The database session to use for the operation.

    Returns:
        UserRetrieveSchema: The newly registered user.
    """
    user = await register_user_in_db(form, db)
    return UserRetrieveSchema.from_orm(user)


@router.post("/login", response_model=TokenSchema)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Look up user by email (case-insensitive)
    # Note: OAuth2PasswordRequestForm uses "username" field, but we treat it as email
    result = await db.execute(
        select(DbUser).where(
            func.lower(DbUser.email) == form_data.username.lower(),
        ),
    )
    user = result.scalars().first()

    # Verify user exists and password is correct
    # Don't reveal which one failed (security best practice)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user id as subject
    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRetrieveSchema)
async def get_current_user(current_user: Annotated[DbUser, Depends(get_current_user_from_db)]):
    return current_user

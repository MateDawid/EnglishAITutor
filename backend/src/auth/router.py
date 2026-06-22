from typing import Annotated

from auth.services.user_services.current_user_service import get_current_user_from_db
from auth.services.user_services.register_user_service import register_user
from auth.services.user_services.login_user_service import login_user
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.schemas import TokenSchema, UserCreateSchema, UserRetrieveSchema
from auth.models import DbUser


router = APIRouter()


@router.post("/register", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def register_user_view(form: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> UserRetrieveSchema:
    """
    View to register a new user in the database.

    Args:
        form (UserCreateSchema): The user data to register.
        db (AsyncSession): The database session to use for the operation.

    Returns:
        UserRetrieveSchema: The newly registered user.
    """
    user = await register_user(form, db)
    return UserRetrieveSchema.from_orm(user)


@router.post("/login", response_model=TokenSchema)
async def login_user_view(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenSchema:
    """
    View to authenticate the user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username (email) and password.
        db (AsyncSession): The database session to use for the query.
    
    Returns:
        TokenSchema: The access token and token type if authentication is successful.
    """
    return await login_user(form_data, db)
    

@router.get("/me", response_model=UserRetrieveSchema)
async def current_user_view(current_user: Annotated[DbUser, Depends(get_current_user_from_db)]) -> UserRetrieveSchema:
    """
    View to retrieve the current authenticated user's information.

    Args:
        current_user (DbUser): The current authenticated user.

    Returns:
        UserRetrieveSchema: The current user's information.
    """
    return UserRetrieveSchema.from_orm(current_user)

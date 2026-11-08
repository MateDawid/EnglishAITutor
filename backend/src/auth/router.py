from typing import Annotated

from auth.services.current_user_service import get_current_user_from_db
from auth.constants import ACCESS_TOKEN_COOKIE_NAME, ACCESS_TOKEN_EXPIRE_SECONDS
from auth.services.csrf_service import create_csrf_token
from auth.services.register_user_service import register_user
from auth.services.login_user_service import login_user
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_db
from auth.schemas import UserCreateSchema, UserRetrieveSchema
from auth.models import DbUser
from auth.services.token_service import create_access_token


router = APIRouter()


@router.post("/register", response_model=UserRetrieveSchema, status_code=status.HTTP_201_CREATED)
async def register_user_view(
    form: UserCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserRetrieveSchema:
    """
    View to register a new user in the database.

    Args:
        form (UserCreateSchema): The user data to register.
        db (AsyncSession): The database session to use for the operation.

    Returns:
        UserRetrieveSchema: The newly registered user.
    """
    user = await register_user(form, db)
    return UserRetrieveSchema.model_validate(user, from_attributes=True)


@router.get("/csrf")
async def csrf_token_view() -> dict[str, str]:
    """
    Issue a signed CSRF token for the browser to send on unsafe requests.

    Returns:
        dict[str, str]: The signed CSRF token.
    """
    return {"csrf_token": create_csrf_token()}


@router.post("/login", response_model=UserRetrieveSchema)
async def login_user_view(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
) -> UserRetrieveSchema:
    """
    Authenticate the user and establish a cookie-based browser session.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username (email) and password.
        db (AsyncSession): The database session to use for the query.
        response (Response): The HTTP response used to set the access cookie.

    Returns:
        UserRetrieveSchema: The authenticated user's information.
    """
    user = await login_user(form_data, db)
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=create_access_token(data={"sub": str(user.id)}),
        max_age=ACCESS_TOKEN_EXPIRE_SECONDS,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return UserRetrieveSchema.model_validate(user, from_attributes=True)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user_view(response: Response) -> None:
    """
    Clear the browser's access-token cookie.

    Args:
        response (Response): The HTTP response used to clear the cookie.
    """
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )


@router.get("/me", response_model=UserRetrieveSchema)
async def current_user_view(current_user: Annotated[DbUser, Depends(get_current_user_from_db)]) -> UserRetrieveSchema:
    """
    View to retrieve the current authenticated user's information.

    Args:
        current_user (DbUser): The current authenticated user.

    Returns:
        UserRetrieveSchema: The current user's information.
    """
    return UserRetrieveSchema.model_validate(current_user, from_attributes=True)

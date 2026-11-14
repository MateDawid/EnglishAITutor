from datetime import UTC, datetime

import jwt
import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from auth.constants import (
    ACCESS_TOKEN_COOKIE_NAME,
    ACCESS_TOKEN_EXPIRE_SECONDS,
    CSRF_TOKEN_EXPIRE_SECONDS,
)
from auth.models import DbUser
from auth.services.csrf_service import verify_csrf_token
from auth.services.token_service import create_access_token, hash_password
from config import settings
from factories.user import UserFactory


@pytest.mark.asyncio
class TestRegisterUserView:
    """
    Tests for register_user_view endpoint.
    """

    async def test_register_user_success(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Valid registration data.
        WHEN: POST /auth/register is called.
        THEN: A new user is created and returned.
        """
        response = await client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password_1": "password",
                "password_2": "password",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()

        assert data["email"] == "test@example.com"
        assert "id" in data

    async def test_register_user_returns_400_when_email_exists(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing user email.
        WHEN: POST /auth/register is called.
        THEN: An error response is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(email="test@example.com")

        response = await client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password_1": "password",
                "password_2": "password",
            },
        )

        assert response.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_409_CONFLICT,
        )

    async def test_register_user_returns_400_when_passwords_do_not_match(
        self,
        client,
    ):
        """
        GIVEN: Non-matching passwords.
        WHEN: POST /auth/register is called.
        THEN: An error response is returned.
        """
        response = await client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password_1": "password",
                "password_2": "different-password",
            },
        )

        assert response.status_code >= 400

    async def test_register_user_normalizes_email(
        self,
        client,
    ):
        """
        GIVEN: An email with uppercase characters.
        WHEN: POST /auth/register is called.
        THEN: The email is returned in lowercase.
        """
        response = await client.post(
            "/auth/register",
            json={
                "email": "Test.User@Example.COM",
                "password_1": "password",
                "password_2": "password",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()

        assert data["email"] == "test.user@example.com"


@pytest.mark.asyncio
class TestLoginUserView:
    """
    Tests for login_user_view endpoint.
    """

    async def test_login_user_success(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Valid user credentials.
        WHEN: POST /auth/login is called.
        THEN: The user is returned and a secure session cookie is set.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory.build(email="test@example.com", password_hash=hash_password("password"))
        db_session.add(created_user)
        await db_session.flush()

        response = await client.post(
            "/auth/login",
            data={
                "username": "test@example.com",
                "password": "password",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["id"] == str(created_user.id)
        assert data["email"] == "test@example.com"
        assert "access_token" not in data
        cookie = response.headers["set-cookie"]
        assert f"{ACCESS_TOKEN_COOKIE_NAME}=" in cookie
        assert f"Max-Age={ACCESS_TOKEN_EXPIRE_SECONDS}" in cookie
        assert "HttpOnly" in cookie
        assert "Secure" in cookie
        assert "SameSite=lax" in cookie
        assert "Path=/" in cookie
        assert "Domain=" not in cookie

    async def test_login_user_returns_error_for_invalid_password(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Existing user and wrong password.
        WHEN: POST /auth/login is called.
        THEN: An authentication error is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email="test@example.com",
            password_hash=hash_password("correct-password"),
        )

        response = await client.post(
            "/auth/login",
            data={
                "username": "test@example.com",
                "password": "wrong-password",
            },
        )

        assert response.status_code >= 400

    async def test_login_user_returns_error_for_unknown_user(
        self,
        client,
    ):
        """
        GIVEN: A non-existing user.
        WHEN: POST /auth/login is called.
        THEN: An authentication error is returned.
        """
        response = await client.post(
            "/auth/login",
            data={
                "username": "missing@example.com",
                "password": "password",
            },
        )

        assert response.status_code >= 400

    async def test_login_user_is_case_insensitive(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Existing user with mixed-case email.
        WHEN: Login is attempted with different casing.
        THEN: Authentication succeeds.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email="Test.User@Example.com",
            password_hash=hash_password("password"),
        )

        response = await client.post(
            "/auth/login",
            data={
                "username": "test.user@example.com",
                "password": "password",
            },
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestCurrentUserView:
    """
    Tests for current_user_view endpoint.
    """

    async def test_current_user_success(
        self,
        client,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A valid authentication token.
        WHEN: GET /auth/me is called.
        THEN: The current user information is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        user = UserFactory.build()
        db_session.add(user)
        await db_session.flush()

        token = create_access_token(
            data={"sub": str(user.id)},
        )
        client.cookies.set(ACCESS_TOKEN_COOKIE_NAME, token, path="/")

        response = await client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["id"] == str(user.id)
        assert data["email"] == user.email

    async def test_current_user_returns_401_for_missing_token(
        self,
        client,
    ):
        """
        GIVEN: No authentication token.
        WHEN: GET /auth/me is called.
        THEN: Unauthorized is returned.
        """
        response = await client.get("/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_current_user_returns_401_for_invalid_token(
        self,
        client,
    ):
        """
        GIVEN: An invalid authentication token.
        WHEN: GET /auth/me is called.
        THEN: Unauthorized is returned.
        """
        response = await client.get(
            "/auth/me",
            headers={
                "Authorization": "Bearer invalid-token",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_current_user_returns_not_found_for_missing_user(
        self,
        client,
    ):
        """
        GIVEN: A valid token containing a non-existing user id.
        WHEN: GET /auth/me is called.
        THEN: User not found error is returned.
        """
        token = create_access_token(
            data={
                "sub": "11111111-1111-1111-1111-111111111111",
            },
        )
        client.cookies.set(ACCESS_TOKEN_COOKIE_NAME, token, path="/")

        response = await client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code >= 400


@pytest.mark.asyncio
async def test_csrf_bootstrap_returns_signed_token(client: AsyncClient) -> None:
    """
    GIVEN: A browser requests a CSRF bootstrap token.
    WHEN: GET /auth/csrf is called.
    THEN: A valid signed CSRF token is returned.
    """
    response = await client.get("/auth/csrf")

    assert response.status_code == status.HTTP_200_OK
    csrf_token = response.json()["csrf_token"]
    assert verify_csrf_token(csrf_token)

    payload = jwt.decode(
        csrf_token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.algorithm],
    )
    remaining_seconds = payload["exp"] - datetime.now(UTC).timestamp()
    assert CSRF_TOKEN_EXPIRE_SECONDS - 1 <= remaining_seconds <= CSRF_TOKEN_EXPIRE_SECONDS


@pytest.mark.asyncio
async def test_unsafe_request_rejects_untrusted_origin(client: AsyncClient) -> None:
    """
    GIVEN: A state-changing request from an untrusted origin.
    WHEN: POST /auth/register is called.
    THEN: The request is rejected.
    """
    response = await client.post(
        "/auth/register",
        json={
            "email": "untrusted@example.com",
            "password_1": "password",
            "password_2": "password",
        },
        headers={"Origin": "https://untrusted.example"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_unsafe_request_rejects_missing_origin(client: AsyncClient) -> None:
    """
    GIVEN: A state-changing request without an origin.
    WHEN: POST /auth/register is called.
    THEN: The request is rejected.
    """
    response = await client.post(
        "/auth/register",
        json={
            "email": "missing-origin@example.com",
            "password_1": "password",
            "password_2": "password",
        },
        headers={"Origin": ""},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_unsafe_request_rejects_missing_csrf_token(client: AsyncClient) -> None:
    """
    GIVEN: A state-changing request without a CSRF token.
    WHEN: POST /auth/register is called.
    THEN: The request is rejected.
    """
    response = await client.post(
        "/auth/register",
        json={
            "email": "missing-csrf@example.com",
            "password_1": "password",
            "password_2": "password",
        },
        headers={"X-CSRF-Token": ""},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_unsafe_request_rejects_access_token_as_csrf_token(client: AsyncClient) -> None:
    """
    GIVEN: A state-changing request with an access token in the CSRF header.
    WHEN: POST /auth/register is called.
    THEN: The request is rejected.
    """
    access_token = create_access_token(data={"sub": "user"})
    response = await client.post(
        "/auth/register",
        json={
            "email": "wrong-csrf@example.com",
            "password_1": "password",
            "password_2": "password",
        },
        headers={"X-CSRF-Token": access_token},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_logout_clears_access_cookie(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """
    GIVEN: A user with an authenticated cookie session.
    WHEN: POST /auth/logout is called.
    THEN: The access cookie is cleared.
    """
    UserFactory._meta.sqlalchemy_session = db_session
    UserFactory(email="logout@example.com", password_hash=hash_password("password"))

    await client.post(
        "/auth/login",
        data={"username": "logout@example.com", "password": "password"},
    )
    response = await client.post("/auth/logout")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "Max-Age=0" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "Secure" in response.headers["set-cookie"]
    assert "SameSite=lax" in response.headers["set-cookie"]

    current_user_response = await client.get("/auth/me")
    assert current_user_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_current_user_does_not_accept_bearer_authentication(
    client: AsyncClient,
    test_user: DbUser,
) -> None:
    """
    GIVEN: A valid bearer token without an access cookie.
    WHEN: GET /auth/me is called.
    THEN: The request is unauthorized.
    """
    token = create_access_token(data={"sub": str(test_user.id)})

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

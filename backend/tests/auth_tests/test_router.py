import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.services.token_service import create_access_token, verify_password, hash_password
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
        THEN: A token is returned.
        """
        # UserFactory._meta.sqlalchemy_session = db_session
        # UserFactory(
        #     email="test@example.com",
        #     password_hash="password",
        # )
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory.build(
            email="test@example.com",
            password_hash=hash_password("password")
        )
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

        assert "access_token" in data
        assert data["token_type"] == "bearer"

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

        response = await client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code >= 400
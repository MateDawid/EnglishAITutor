import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.db_user import DbUser
from auth.schemas import TokenSchema
from auth.services.token_service import create_access_token
from auth.services.exceptions import InvalidCredentialsException
from auth.services.login_user_service import (
    get_user_from_db_by_email,
    login_user,
)
from factories.user import UserFactory


@pytest.mark.asyncio
class TestGetUserFromDbByEmailFunction:
    """
    Tests for get_user_from_db_by_email function.
    """

    async def test_get_user_from_db_by_email_returns_user(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing user email.
        WHEN: The user is fetched by email.
        THEN: The corresponding DbUser instance is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory(email="test@example.com")

        user = await get_user_from_db_by_email(
            "test@example.com",
            db_session,
        )

        assert isinstance(user, DbUser)
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_user_from_db_by_email_is_case_insensitive(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing user email with mixed casing.
        WHEN: The user is fetched using a different casing.
        THEN: The user is found and returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory(email="Test.User@Example.com")

        user = await get_user_from_db_by_email(
            "test.user@example.com",
            db_session,
        )

        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_user_from_db_by_email_returns_none_when_not_found(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A non-existing email.
        WHEN: The user is fetched by email.
        THEN: None is returned.
        """
        user = await get_user_from_db_by_email(
            "missing@example.com",
            db_session,
        )

        assert user is None


@pytest.mark.asyncio
class TestLoginUserFunction:
    """
    Tests for login_user function.
    """

    async def test_login_user_success(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Valid user credentials.
        WHEN: The login service is called.
        THEN: A valid TokenSchema is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email="test@example.com",
            password="password",
        )

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com",
            password="password",
            scope="",
        )

        token = await login_user(form_data, db_session)

        assert isinstance(token, TokenSchema)
        assert token.token_type == "bearer"
        assert isinstance(token.access_token, str)
        assert len(token.access_token) > 0

    async def test_login_user_success_with_case_insensitive_email(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A user with a mixed-case email.
        WHEN: Login is attempted using a different casing.
        THEN: Authentication succeeds.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email="Test.User@Example.com",
            password="password",
        )

        form_data = OAuth2PasswordRequestForm(
            username="test.user@example.com",
            password="password",
            scope="",
        )

        token = await login_user(form_data, db_session)

        assert isinstance(token, TokenSchema)
        assert token.token_type == "bearer"

    async def test_login_user_returns_expected_token(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Valid user credentials.
        WHEN: The login service is called.
        THEN: The generated access token contains the expected user id.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        user = UserFactory(
            email="test@example.com",
            password="password",
        )

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com",
            password="password",
            scope="",
        )

        token = await login_user(form_data, db_session)

        expected_token = create_access_token(
            data={"sub": str(user.id)},
        )

        assert token.access_token == expected_token
        assert token.token_type == "bearer"

    async def test_login_user_raises_for_non_existing_user(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An email that does not exist.
        WHEN: Login is attempted.
        THEN: InvalidCredentialsException is raised.
        """
        form_data = OAuth2PasswordRequestForm(
            username="missing@example.com",
            password="password",
            scope="",
        )

        with pytest.raises(InvalidCredentialsException):
            await login_user(form_data, db_session)

    async def test_login_user_raises_for_invalid_password(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing user and an incorrect password.
        WHEN: Login is attempted.
        THEN: InvalidCredentialsException is raised.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email="test@example.com",
            password="correct-password",
        )

        form_data = OAuth2PasswordRequestForm(
            username="test@example.com",
            password="wrong-password",
            scope="",
        )

        with pytest.raises(InvalidCredentialsException):
            await login_user(form_data, db_session)

    @pytest.mark.parametrize(
        "email",
        [
            "test@example.com",
            "Test@Example.com",
            "TEST@EXAMPLE.COM",
        ],
    )
    async def test_login_user_raises_for_invalid_password_regardless_of_email_case(
        self,
        db_session: AsyncSession,
        email: str,
    ):
        """
        GIVEN: An existing user.
        WHEN: Login is attempted with an incorrect password.
        THEN: InvalidCredentialsException is raised.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(
            email=email,
            password="correct-password",
        )

        form_data = OAuth2PasswordRequestForm(
            username=email.lower(),
            password="invalid-password",
            scope="",
        )

        with pytest.raises(InvalidCredentialsException):
            await login_user(form_data, db_session)

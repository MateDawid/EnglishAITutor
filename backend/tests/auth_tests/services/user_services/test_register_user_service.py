import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.models.db_user import DbUser
from auth.schemas.user_create_schema import UserCreateSchema
from auth.services.token_service import verify_password
from auth.services.exceptions import (
    PasswordMismatchException,
    UserAlreadyExistsException,
)
from auth.services.register_user_service import (
    save_user_in_db,
    validate_user_passwords,
    register_user,
    validate_user_email_uniqueness,
)
from factories.user import UserFactory


@pytest.mark.asyncio
class TestValidateUserEmailUniquenessFunction:
    """
    Tests for validate_user_email_uniqueness function.
    """

    async def test_validate_user_email_uniqueness_success(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An email that does not exist.
        WHEN: Email uniqueness is validated.
        THEN: No exception is raised.
        """
        await validate_user_email_uniqueness(
            "test@example.com",
            db_session,
        )

    async def test_validate_user_email_uniqueness_raises_for_existing_email(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing email.
        WHEN: Email uniqueness is validated.
        THEN: UserAlreadyExistsException is raised.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(email="test@example.com")

        with pytest.raises(UserAlreadyExistsException):
            await validate_user_email_uniqueness(
                "test@example.com",
                db_session,
            )

    async def test_validate_user_email_uniqueness_raises_case_insensitive(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing email with different casing.
        WHEN: Email uniqueness is validated.
        THEN: UserAlreadyExistsException is raised.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(email="Test@Example.com")

        with pytest.raises(UserAlreadyExistsException):
            await validate_user_email_uniqueness(
                "test@example.com",
                db_session,
            )


class TestValidateUserPasswordsFunction:
    """
    Tests for validate_user_passwords function.
    """

    def test_validate_user_passwords_success(self):
        """
        GIVEN: Matching passwords.
        WHEN: Password validation is performed.
        THEN: No exception is raised.
        """
        validate_user_passwords("password", "password")

    def test_validate_user_passwords_raises_for_mismatch(self):
        """
        GIVEN: Non-matching passwords.
        WHEN: Password validation is performed.
        THEN: PasswordMismatchException is raised.
        """
        with pytest.raises(PasswordMismatchException):
            validate_user_passwords("password", "different")


@pytest.mark.asyncio
class TestSaveUserInDbFunction:
    """
    Tests for save_user_in_db function.
    """

    async def test_save_user_in_db_success(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Valid user data.
        WHEN: The user is saved.
        THEN: A DbUser instance is returned.
        """
        form = UserCreateSchema(
            email="Test@Example.com",
            password_1="password",
            password_2="password",
        )

        user = await save_user_in_db(form, db_session)

        assert isinstance(user, DbUser)
        assert user.id is not None
        assert user.email == "test@example.com"
        assert verify_password(
            form.password_1,
            user.password_hash,
        )

        result = await db_session.execute(select(DbUser).where(DbUser.email == user.email))
        db_user = result.scalar_one_or_none()

        assert db_user is not None
        assert db_user.id == user.id
        assert db_user.email == user.email


@pytest.mark.asyncio
class TestRegisterUserFunction:
    """
    Tests for register_user function.
    """

    async def test_register_user_success(self, db_session: AsyncSession):
        """
        GIVEN: A valid user registration form.
        WHEN: The user registration service is called.
        THEN: A new user is created and returned.
        """
        form = UserCreateSchema(
            email="test@example.com",
            password_1="password",
            password_2="password",
        )

        user = await register_user(form, db_session)

        assert user.email == form.email
        assert verify_password(form.password_1, user.password_hash)

    @pytest.mark.parametrize(
        "email",
        [
            "test@example.com",
            "Test@Example.com",
        ],
    )
    async def test_register_user_raises_when_email_already_exists(self, db_session: AsyncSession, email: str):
        """
        GIVEN: An existing user with the same email.
        WHEN: The user registration service is called.
        THEN: UserAlreadyExistsException is raised.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        UserFactory(email=email)

        form = UserCreateSchema(
            email=email,
            password_1="password",
            password_2="password",
        )

        with pytest.raises(UserAlreadyExistsException):
            await register_user(form, db_session)

    async def test_register_user_raises_when_passwords_do_not_match(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A registration form with different passwords.
        WHEN: The user registration service is called.
        THEN: PasswordMismatchException is raised.
        """
        form = UserCreateSchema(
            email="test@example.com",
            password_1="password123",
            password_2="different-password",
        )

        with pytest.raises(PasswordMismatchException):
            await register_user(form, db_session)

    async def test_register_user_normalizes_email_to_lowercase(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A registration form with an uppercase email.
        WHEN: The user registration service is called.
        THEN: The stored email is converted to lowercase.
        """
        form = UserCreateSchema(
            email="Test.User@Example.COM",
            password_1="password",
            password_2="password",
        )

        user = await register_user(form, db_session)

        assert user.email == "test.user@example.com"

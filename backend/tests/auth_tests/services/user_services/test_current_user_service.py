import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models.db_user import DbUser
from auth.services.token_service import create_access_token
from auth.services.current_user_service import (
    get_current_user_from_db,
    get_db_user_by_id,
    get_user_id_from_token,
)
from auth.services.exceptions import (
    InvalidTokenException,
    UserNotFoundException,
)
from factories.user import UserFactory


class TestGetUserIdFromTokenFunction:
    """
    Tests for get_user_id_from_token function.
    """

    def test_get_user_id_from_token_success(self):
        """
        GIVEN: A valid access token.
        WHEN: The user id is extracted from the token.
        THEN: The UUID contained in the token is returned.
        """
        user_id = uuid.uuid4()

        token = create_access_token(
            data={"sub": str(user_id)},
        )

        result = get_user_id_from_token(token)

        assert result == user_id
        assert isinstance(result, uuid.UUID)

    def test_get_user_id_from_token_raises_for_invalid_token(self):
        """
        GIVEN: An invalid token.
        WHEN: The user id is extracted.
        THEN: InvalidTokenException is raised.
        """
        with pytest.raises(InvalidTokenException):
            get_user_id_from_token("invalid-token")

    def test_get_user_id_from_token_raises_for_token_without_uuid(self):
        """
        GIVEN: A token with a non-UUID subject.
        WHEN: The user id is extracted.
        THEN: InvalidTokenException is raised.
        """
        token = create_access_token(
            data={"sub": "not-a-uuid"},
        )

        with pytest.raises(InvalidTokenException):
            get_user_id_from_token(token)

    @pytest.mark.parametrize(
        "subject",
        [
            "",
            "123",
            "user-id",
            "invalid-uuid-value",
        ],
    )
    def test_get_user_id_from_token_raises_for_malformed_uuid(
        self,
        subject: str,
    ):
        """
        GIVEN: A token containing an invalid UUID value.
        WHEN: The user id is extracted.
        THEN: InvalidTokenException is raised.
        """
        token = create_access_token(
            data={"sub": subject},
        )

        with pytest.raises(InvalidTokenException):
            get_user_id_from_token(token)


@pytest.mark.asyncio
class TestGetDbUserByIdFunction:
    """
    Tests for get_db_user_by_id function.
    """

    async def test_get_db_user_by_id_success(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An existing user id.
        WHEN: The user is fetched from the database.
        THEN: The corresponding DbUser instance is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory.build()
        db_session.add(created_user)
        await db_session.flush()

        user = await get_db_user_by_id(
            created_user.id,
            db_session,
        )

        assert isinstance(user, DbUser)
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_db_user_by_id_raises_when_user_does_not_exist(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A non-existing user id.
        WHEN: The user is fetched from the database.
        THEN: UserNotFoundException is raised.
        """
        with pytest.raises(UserNotFoundException):
            await get_db_user_by_id(
                uuid.uuid4(),
                db_session,
            )


@pytest.mark.asyncio
class TestGetCurrentUserFromDbFunction:
    """
    Tests for get_current_user_from_db function.
    """

    async def test_get_current_user_from_db_success(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A valid token for an existing user.
        WHEN: The current user is requested.
        THEN: The corresponding DbUser is returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        created_user = UserFactory.build()
        db_session.add(created_user)
        await db_session.flush()

        token = create_access_token(
            data={"sub": str(created_user.id)},
        )

        user = await get_current_user_from_db(
            token,
            db_session,
        )

        assert isinstance(user, DbUser)
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_current_user_from_db_raises_for_invalid_token(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An invalid token.
        WHEN: The current user is requested.
        THEN: InvalidTokenException is raised.
        """
        with pytest.raises(InvalidTokenException):
            await get_current_user_from_db(
                "invalid-token",
                db_session,
            )

    async def test_get_current_user_from_db_raises_when_user_does_not_exist(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A valid token containing a non-existing user id.
        WHEN: The current user is requested.
        THEN: UserNotFoundException is raised.
        """
        token = create_access_token(
            data={"sub": str(uuid.uuid4())},
        )

        with pytest.raises(UserNotFoundException):
            await get_current_user_from_db(
                token,
                db_session,
            )

    async def test_get_current_user_from_db_raises_for_invalid_uuid_in_token(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A token containing a non-UUID subject.
        WHEN: The current user is requested.
        THEN: InvalidTokenException is raised.
        """
        token = create_access_token(
            data={"sub": "not-a-uuid"},
        )

        with pytest.raises(InvalidTokenException):
            await get_current_user_from_db(
                token,
                db_session,
            )

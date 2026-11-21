from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from conversations.models import DbConversation
from conversations.schemas import ConversationSchema
from conversations.services.conversation_service import get_conversations_from_db
from factories.user import UserFactory
from utils.pagination import PaginatedResponse, PaginationQuery


@pytest.mark.asyncio
class TestGetConversationsFromDbFunction:
    """Tests for get_conversations_from_db."""

    async def test_get_conversations_from_db_filters_orders_and_paginates(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ) -> None:
        """
        GIVEN: Conversations for multiple users with different update times.
        WHEN: Conversations are requested across pages.
        THEN: Only the current user's conversations are returned, newest first.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        other_user = UserFactory.build(email="other@example.com")
        db_session.add(other_user)
        await db_session.flush()

        earlier = datetime(2026, 10, 24, 8, 30, tzinfo=UTC)
        later = datetime(2026, 10, 24, 8, 35, tzinfo=UTC)
        db_session.add_all(
            [
                DbConversation(
                    user_id=test_user.id,
                    title="Earlier",
                    created_at=earlier,
                    updated_at=earlier,
                ),
                DbConversation(
                    user_id=test_user.id,
                    title="Later",
                    created_at=earlier,
                    updated_at=later,
                ),
                DbConversation(
                    user_id=other_user.id,
                    title="Not mine",
                    created_at=later,
                    updated_at=later,
                ),
            ]
        )
        await db_session.flush()

        first_page = await get_conversations_from_db(
            db=db_session,
            user=test_user,
            pagination_query=PaginationQuery(page=1, page_size=1),
        )
        second_page = await get_conversations_from_db(
            db=db_session,
            user=test_user,
            pagination_query=PaginationQuery(page=2, page_size=1),
        )

        assert isinstance(first_page, PaginatedResponse)
        assert first_page.total == 2
        assert first_page.items[0].title == "Later"
        assert isinstance(first_page.items[0], ConversationSchema)
        assert second_page.total == 2
        assert second_page.items[0].title == "Earlier"

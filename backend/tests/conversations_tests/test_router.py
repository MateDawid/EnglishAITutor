from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from conversations.models import DbConversation
from factories.user import UserFactory


class TestConversationListView:
    """Tests for GET /conversations."""

    async def test_list_view_returns_only_authenticated_users_conversations(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
        test_user: DbUser,
    ) -> None:
        """
        GIVEN: Conversations belonging to the authenticated user and another user.
        WHEN: GET /conversations is called.
        THEN: Only the authenticated user's paginated conversations are returned.
        """
        UserFactory._meta.sqlalchemy_session = db_session
        other_user = UserFactory.build(email="other@example.com")
        db_session.add(other_user)
        await db_session.flush()

        own_conversation = DbConversation(user_id=test_user.id, title="My practice")
        other_conversation = DbConversation(user_id=other_user.id, title="Other practice")
        db_session.add_all([own_conversation, other_conversation])
        await db_session.flush()

        response = await authenticated_client.get("/conversations?page=1&page_size=1")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["page"] == 1
        assert data["page_size"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == str(own_conversation.id)
        assert data["items"][0]["title"] == "My practice"
        assert "created_at" in data["items"][0]
        assert "updated_at" in data["items"][0]

    async def test_list_view_requires_authentication(
        self,
        client: AsyncClient,
    ) -> None:
        """
        GIVEN: A request without authentication.
        WHEN: GET /conversations is called.
        THEN: 401 Unauthorized is returned.
        """
        response = await client.get("/conversations")

        assert response.status_code == 401

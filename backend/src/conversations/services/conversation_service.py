from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from conversations.models import DbConversation
from conversations.schemas import ConversationCreateSchema, ConversationSchema
from utils.pagination import PaginatedResponse, PaginationQuery, get_paginated_response


async def create_conversation_in_db(
    db: AsyncSession,
    user: DbUser,
    conversation: ConversationCreateSchema,
) -> ConversationSchema:
    """
    Create a conversation for the authenticated user.

    Args:
        db (AsyncSession): The database session to use for the operation.
        user (DbUser): The current authenticated user.
        conversation (ConversationCreateSchema): The conversation data to create.

    Returns:
        ConversationSchema: The newly created conversation.
    """
    db_conversation = DbConversation(user_id=user.id, title=conversation.title)
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return ConversationSchema.model_validate(db_conversation)


async def get_conversations_from_db(
    db: AsyncSession,
    user: DbUser,
    pagination_query: PaginationQuery,
) -> PaginatedResponse[ConversationSchema]:
    """
    Get the authenticated user's conversations from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        user (DbUser): The current authenticated user.
        pagination_query (PaginationQuery): The pagination query parameters.

    Returns:
        PaginatedResponse[ConversationSchema]: The user's paginated conversations.
    """
    query = (
        select(DbConversation)
        .where(DbConversation.user_id == user.id)
        .order_by(DbConversation.updated_at.desc(), DbConversation.id.desc())
    )
    return await get_paginated_response(
        db=db,
        query=query,
        schema_type=ConversationSchema,
        pagination_query=pagination_query,
    )

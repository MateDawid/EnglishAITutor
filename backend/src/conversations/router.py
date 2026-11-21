from typing import Annotated

from auth.models import DbUser
from auth.services.current_user_service import get_current_user_from_db
from conversations.schemas import ConversationSchema
from conversations.services.conversation_service import get_conversations_from_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils.database import get_db
from utils.pagination import PaginatedResponse, PaginationQuery

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ConversationSchema], status_code=status.HTTP_200_OK)
async def conversation_list_view(
    user: Annotated[DbUser, Depends(get_current_user_from_db)],
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination_query: Annotated[PaginationQuery, Depends()],
) -> PaginatedResponse[ConversationSchema]:
    """
    Retrieve the current user's conversations.

    Args:
        user (DbUser): The current authenticated user.
        db (AsyncSession): The database session.
        pagination_query (PaginationQuery): The pagination query parameters.

    Returns:
        PaginatedResponse[ConversationSchema]: The user's paginated conversations.
    """
    return await get_conversations_from_db(db=db, user=user, pagination_query=pagination_query)

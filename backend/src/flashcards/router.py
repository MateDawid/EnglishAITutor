from typing import Annotated

# from flashcards.services.flashcard_service import get_flashcards_from_db

from auth.models import DbUser
from auth.services.current_user_service import get_current_user_from_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_db
from flashcards.schemas import FlashcardSchema
from flashcards.services.flashcard_service import get_flashcards_from_db
from pagination import PaginationQuery, PaginatedResponse
from utils.sorting import OrderByField, OrderByQuery

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[FlashcardSchema], status_code=status.HTTP_200_OK)
async def flashcard_list_view(
    _: Annotated[DbUser, Depends(get_current_user_from_db)],
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination_query: Annotated[PaginationQuery, Depends()],
    order_by: Annotated[OrderByField, OrderByQuery(("word",))],
) -> PaginatedResponse[FlashcardSchema]:
    """
    View to retrieve the list of flashcards.

    Args:
        _ (DbUser): The current authenticated user.
        db (AsyncSession): The database session.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    return await get_flashcards_from_db(db, pagination_query, order_by)

from typing import Annotated, Optional

from auth.models import DbUser
from auth.services.current_user_service import get_current_user_from_db
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.db_flashcard import PartOfSpeech
from utils.database import get_db
from flashcards.schemas import FlashcardSchema
from flashcards.services.flashcard_service import get_flashcards_from_db
from utils.filtering import FilterByStringQuery
from utils.pagination import PaginationQuery, PaginatedResponse
from utils.sorting import OrderByQuery

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[FlashcardSchema], status_code=status.HTTP_200_OK)
async def flashcard_list_view(
    _: Annotated[DbUser, Depends(get_current_user_from_db)],
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination_query: Annotated[PaginationQuery, Depends()],
    order_by: Annotated[Optional[str], OrderByQuery(("word",))] = None,
    word: Annotated[Optional[str], FilterByStringQuery()] = None,
    meaning: Annotated[Optional[str], FilterByStringQuery()] = None,
    part_of_speech: Annotated[Optional[PartOfSpeech], Query()] = None,
) -> PaginatedResponse[FlashcardSchema]:
    """
    View to retrieve the list of flashcards.

    Args:
        _ (DbUser): The current authenticated user.
        db (AsyncSession): The database session.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.
        word (str | None): The "word" field filter.
        meaning (str | None): The "meaning" field filter.
        part_of_speech (str | None): The "part_of_speech" field filter.
    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    return await get_flashcards_from_db(
        db=db,
        pagination_query=pagination_query,
        order_by=order_by,
        filters={"word": word, "meaning": meaning, "part_of_speech": part_of_speech},
    )

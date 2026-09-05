from typing import Annotated, Optional
from uuid import UUID

from auth.models import DbUser
from auth.services.current_user_service import get_current_user_from_db
from fastapi import APIRouter, Depends, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.enums import RatingFilter, DatabaseRating
from flashcards.models.db_flashcard import PartOfSpeech
from utils.database import get_db
from flashcards.schemas import FlashcardSchema, UserRatingSchema
from flashcards.services.flashcard_service import get_flashcards_from_db, update_or_create_user_rating
from utils.filtering import FilterByStringQuery
from utils.pagination import PaginationQuery, PaginatedResponse
from utils.sorting import OrderByQuery

router = APIRouter()


def _rating_filter_description() -> str:
    """
    Generate a description string for the rating filter query parameter.

    Returns:
        str: The description string.
    """
    return ", ".join([f"{rating_filter.name}={rating_filter.value}" for rating_filter in list(RatingFilter)])


@router.get("/", response_model=PaginatedResponse[FlashcardSchema], status_code=status.HTTP_200_OK)
async def flashcard_list_view(
    user: Annotated[DbUser, Depends(get_current_user_from_db)],
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination_query: Annotated[PaginationQuery, Depends()],
    order_by: Annotated[Optional[str], OrderByQuery(("word",))] = None,
    word: Annotated[Optional[str], FilterByStringQuery()] = None,
    meaning: Annotated[Optional[str], FilterByStringQuery()] = None,
    part_of_speech: Annotated[Optional[PartOfSpeech], Query()] = None,
    rating: Annotated[Optional[RatingFilter], Query(description=_rating_filter_description())] = None,
) -> PaginatedResponse[FlashcardSchema]:
    """
    View to retrieve the list of flashcards.

    Args:
        user (DbUser): The current authenticated user.
        db (AsyncSession): The database session.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.
        word (str | None): The "word" field filter.
        meaning (str | None): The "meaning" field filter.
        part_of_speech (PartOfSpeech | None): The "part_of_speech" field filter.
        rating (Rating | None): The "rating" field filter.
    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    return await get_flashcards_from_db(
        db=db,
        user=user,
        pagination_query=pagination_query,
        order_by=order_by,
        filters={"word": word, "meaning": meaning, "part_of_speech": part_of_speech, "rating": rating},
    )


@router.post("/{flashcard_id}", response_model=UserRatingSchema, status_code=status.HTTP_201_CREATED)
async def rate_flashcard(
    user: Annotated[DbUser, Depends(get_current_user_from_db)],
    db: Annotated[AsyncSession, Depends(get_db)],
    flashcard_id: UUID,
    rating: Annotated[DatabaseRating, Body(embed=True)],
) -> UserRatingSchema:
    """
    View to update or create a user rating for a flashcard.

    Args:
        user (DbUser): The current authenticated user.
        db (AsyncSession): The database session.
        flashcard_id (UUID): The ID of the flashcard to rate.
        rating (DatabaseRating): The rating value (1: EASY, 2: MEDIUM, 3: HARD).

    Returns:
        UserRatingSchema: The user rating schema.
    """
    return await update_or_create_user_rating(db=db, user_id=user.id, flashcard_id=flashcard_id, rating=rating)

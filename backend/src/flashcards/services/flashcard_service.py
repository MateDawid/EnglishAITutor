from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.db_user_rating import Rating
from utils.filtering.services.filtering_service import get_db_query_with_filtering
from utils.sorting import get_db_query_with_ordering
from flashcards.models import DbFlashcard, DbUserRating
from flashcards.schemas import FlashcardSchema, UserRatingSchema
from utils.pagination import get_paginated_response, PaginationQuery, PaginatedResponse


async def get_flashcards_from_db(
    db: AsyncSession,
    pagination_query: PaginationQuery,
    order_by: str | None,
    filters: dict[str, Any],
) -> PaginatedResponse[FlashcardSchema]:
    """
    Get the list of flashcards from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.
        filters (dict[str, Any]): The filters query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    query = select(DbFlashcard)
    query = get_db_query_with_filtering(query=query, filters=filters)
    query = get_db_query_with_ordering(query=query, order_by=order_by)
    response = await get_paginated_response(
        db=db, query=query, schema_type=FlashcardSchema, pagination_query=pagination_query
    )
    return response


async def update_or_create_user_rating(
    db: AsyncSession, user_id: UUID, flashcard_id: UUID, rating: Rating
) -> UserRatingSchema:
    """
    Update or create a user rating for a flashcard.

    Args:
        db (AsyncSession): The database session to use for the query.
        user_id (str): The ID of the user.
        flashcard_id (str): The ID of the flashcard.
        rating (int): The rating value.

    Returns:
        dict: A dictionary containing the status and message of the operation.
    """

    existing_rating = await _get_rating_from_db(db=db, flashcard_id=flashcard_id, user_id=user_id)
    if existing_rating is None:
        db.add(DbUserRating(user_id=user_id, flashcard_id=flashcard_id, rating=rating))
        await db.commit()
        return UserRatingSchema(rating_changed=True)
    if existing_rating.rating == rating:
        return UserRatingSchema(rating_changed=False)
    existing_rating.rating = rating
    await db.commit()
    return UserRatingSchema(rating_changed=True)


async def _get_rating_from_db(db: AsyncSession, flashcard_id: UUID, user_id: UUID) -> DbUserRating | None:
    """
    Get the user rating for a flashcard from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        flashcard_id (UUID): The ID of the flashcard.
        user_id (UUID): The ID of the user.

    Returns:
        DbUserRating | None: The user rating instance if found, otherwise None.
    """
    db_result = await db.execute(
        select(DbUserRating).where(DbUserRating.user_id == user_id, DbUserRating.flashcard_id == flashcard_id)
    )
    return db_result.scalar_one_or_none()

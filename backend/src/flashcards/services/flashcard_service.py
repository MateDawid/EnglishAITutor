from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import with_expression
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from flashcards.enums import RatingFilter, DatabaseRating
from utils.filtering.services.filtering_service import get_db_query_with_filtering
from utils.sorting import get_db_query_with_ordering
from flashcards.models import DbFlashcard, DbUserRating
from flashcards.schemas import FlashcardSchema, UserRatingSchema
from utils.pagination import get_paginated_response, PaginationQuery, PaginatedResponse
from utils.types import SelectType


async def get_flashcards_from_db(
    db: AsyncSession,
    user: DbUser,
    pagination_query: PaginationQuery,
    order_by: str | None,
    filters: dict[str, Any],
) -> PaginatedResponse[FlashcardSchema]:
    """
    Get the list of flashcards from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        user (DbUser): The current authenticated user.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.
        filters (dict[str, Any]): The filters query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    rating_filter = filters.pop("rating", None)

    query = select(DbFlashcard)
    query = _get_db_query_with_user_ratings(query=query, user_id=user.id)
    if rating_filter is not None:
        query = _get_db_query_with_rating_filter(query=query, user_id=user.id, rating=rating_filter)
    query = get_db_query_with_filtering(query=query, filters=filters)
    query = get_db_query_with_ordering(query=query, order_by=order_by)
    response = await get_paginated_response(
        db=db, query=query, schema_type=FlashcardSchema, pagination_query=pagination_query
    )
    return response


def _get_db_query_with_rating_filter(query: SelectType, user_id: UUID, rating: RatingFilter) -> SelectType:
    """
    Filter database query by a specific User rating value.
    Args:
        query (SelectType): The database query to extend.
        user_id (UUID): The ID of the User to get ratings for.
        rating (Rating | None): The rating filter value.

    Returns:
        SelectType: The filtered database query.
    """
    if rating == RatingFilter.NOT_RATED:
        return query.where(
            ~select(DbUserRating.rating)
            .where(
                DbUserRating.flashcard_id == DbFlashcard.id,
                DbUserRating.user_id == user_id,
            )
            .correlate(DbFlashcard)
            .exists()
        )
    return query.where(
        select(DbUserRating.rating)
        .where(
            DbUserRating.flashcard_id == DbFlashcard.id,
            DbUserRating.user_id == user_id,
        )
        .correlate(DbFlashcard)
        .scalar_subquery()
        == rating
    )


def _get_db_query_with_user_ratings(query: SelectType, user_id: UUID) -> SelectType:
    """
    Get the database subquery with User ratings for Flashcards.
    Args:
        query (SelectType): The database query to extend.
        user_id (UUID): The ID of the User to get ratings for.

    Returns:
        SelectType: The database query with User ratings for Flashcards.
    """
    user_rating_subquery = (
        select(DbUserRating.rating)
        .where(
            DbUserRating.flashcard_id == DbFlashcard.id,
            DbUserRating.user_id == user_id,
        )
        .correlate(DbFlashcard)
        .scalar_subquery()
    )
    return query.options(with_expression(DbFlashcard.rating, user_rating_subquery))


async def update_or_create_user_rating(
    db: AsyncSession, user_id: UUID, flashcard_id: UUID, rating: DatabaseRating
) -> UserRatingSchema:
    """
    Update or create a user rating for a flashcard.

    Args:
        db (AsyncSession): The database session to use for the query.
        user_id (UUID): The ID of the user.
        flashcard_id (UUID): The ID of the flashcard.
        rating (DatabaseRating): The rating value.

    Returns:
        UserRatingSchema: A dictionary containing the status and message of the operation.
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

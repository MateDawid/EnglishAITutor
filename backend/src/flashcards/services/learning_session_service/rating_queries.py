"""
This module contains functions to generate database queries for flashcards based on their ratings and the specified
limits. The queries are used to retrieve flashcards for a learning session, prioritizing "hard" rated flashcards,
followed by "medium", "easy", and finally flashcards that have not been rated.
"""

from sqlalchemy import func, select, Select, Subquery
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.enums import DatabaseRating
from flashcards.services.learning_session_service.flashcard_limits import (
    EASY_CARDS_LIMIT,
    MEDIUM_CARDS_LIMIT,
    HARD_CARDS_LIMIT,
    MAX_CARDS,
)

type RatedFlashcardLimits = dict[DatabaseRating | None, int]


async def _get_rated_flashcards_selects(db: AsyncSession, base_flashcard_query: Subquery) -> list[Select]:
    """
    Get the database queries for flashcards based on their ratings and the specified limits.

    Args:
        base_flashcard_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

    Returns:
        list[Select]: A list of database queries for flashcards based on their ratings and the specified limits.
    """
    # Get the limits for the number of flashcards to retrieve for each rating category
    rating_query_limits = await _get_rating_query_limits(db, base_flashcard_query)
    # Create a list of queries for each rating category, limiting the number of flashcards retrieved for each category
    selects = []
    for rating in [*list(DatabaseRating), None]:
        query = _get_rated_flashcards_query(base_flashcard_query, rating, rating_query_limits)
        if query is None:
            continue
        selects.append(query)
    return selects


async def _get_rating_query_limits(db: AsyncSession, base_flashcard_query: Subquery) -> RatedFlashcardLimits:
    """
    Get the limits for the number of flashcards to retrieve for each rating category.

    Returns:
        RatedFlashcardLimits: A dictionary mapping each rating category to its corresponding limit.
    """
    # Get the count of User ratings for each rating category (hard, medium, easy, not rated) from the database
    ratings_count = await _get_ratings_count(db, base_flashcard_query)

    # Calculate the limits for the number of flashcards to retrieve for each rating category based on the
    # total number of flashcards for the learning session and the available flashcards in each category
    remaining_cards_count = MAX_CARDS
    hard_cards_limit = min(HARD_CARDS_LIMIT, ratings_count[DatabaseRating.HARD])
    remaining_cards_count -= hard_cards_limit
    medium_cards_limit = min(MEDIUM_CARDS_LIMIT, ratings_count[DatabaseRating.MEDIUM])
    remaining_cards_count -= medium_cards_limit
    easy_cards_limit = min(EASY_CARDS_LIMIT, ratings_count[DatabaseRating.EASY])
    remaining_cards_count -= easy_cards_limit
    not_rated_cards_limit = min(remaining_cards_count, ratings_count[None])

    return {
        DatabaseRating.HARD: hard_cards_limit,
        DatabaseRating.MEDIUM: medium_cards_limit,
        DatabaseRating.EASY: easy_cards_limit,
        None: not_rated_cards_limit,
    }


async def _get_ratings_count(db: AsyncSession, base_flashcard_query: Subquery) -> RatedFlashcardLimits:
    """
    Get the count of User ratings for each rating category (hard, medium, easy, not rated) from the database.

    Args:
        db (AsyncSession): The database session to use for queries.
        base_flashcard_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

    Returns:
        RatedFlashcardLimits: A dictionary mapping each rating category to its corresponding count.
    """
    ratings_count_query = select(
        base_flashcard_query.c.rating,
        func.count(base_flashcard_query.c.id).label("count"),
    ).group_by(base_flashcard_query.c.rating)
    ratings_count_result = await db.execute(ratings_count_query)
    ratings_count: RatedFlashcardLimits = {
        DatabaseRating.HARD: 0,
        DatabaseRating.MEDIUM: 0,
        DatabaseRating.EASY: 0,
        None: 0,
    }
    for rating, count in ratings_count_result.all():
        ratings_count[rating] = count
    return ratings_count


def _get_rated_flashcards_query(
    flashcards_query: Subquery, rating: DatabaseRating | None, rating_query_limits: RatedFlashcardLimits
) -> Select | None:
    """
    Get the database query for not rated flashcards.

    Args:
        flashcards_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.
        rating (DatabaseRating | None): The rating to filter by (HARD, MEDIUM, EASY, or None for not rated).
        rating_query_limits (RatedFlashcardLimits): Dictionary mapping each rating category to its corresponding limit.

    Returns:
        Select: The database query for not rated flashcards.
    """
    try:
        limit = rating_query_limits[rating]
    except KeyError:
        raise ValueError(f"Invalid rating: {rating}. Must be one of {list(rating_query_limits.keys())}")
    if limit <= 0:
        return None
    return (
        select(flashcards_query.c.id)
        .where(flashcards_query.c.rating.is_(None) if rating is None else flashcards_query.c.rating == rating)
        .order_by(func.random())
        .limit(limit)
    )

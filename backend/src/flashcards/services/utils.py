from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import with_expression

from flashcards.models import DbFlashcard, DbUserRating
from utils.types import SelectType


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

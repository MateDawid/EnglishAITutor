from uuid import UUID

from sqlalchemy import select, ScalarSelect

from flashcards.models import DbFlashcard, DbUserRating


def _get_user_rating_query(user_id: UUID) -> ScalarSelect:
    """
    Get the database subquery with User ratings for Flashcards.
    Args:
        query (SelectType): The database query to extend.
        user_id (UUID): The ID of the User to get ratings for.

    Returns:
        SelectType: The database query with User ratings for Flashcards.
    """
    return (
        select(DbUserRating.rating)
        .where(
            DbUserRating.flashcard_id == DbFlashcard.id,
            DbUserRating.user_id == user_id,
        )
        .correlate(DbFlashcard)
        .scalar_subquery()
    )

from uuid import UUID

from sqlalchemy import select, ScalarSelect

from flashcards.models import DbFlashcard, DbUserRating


def _get_user_rating_query(user_id: UUID) -> ScalarSelect:
    """
    Get the database subquery for User ratings for Flashcards.

    Args:
        user_id (UUID): The ID of the User to get ratings for.

    Returns:
        ScalarSelect: The database query for User ratings for Flashcards.
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

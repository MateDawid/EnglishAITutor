from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from flashcards.schemas import FlashcardSchema


async def get_learning_session_from_db(
    db: AsyncSession,
    user: DbUser,
) -> list[FlashcardSchema]:
    """
    Get the list of flashcards for the learning session from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        user (DbUser): The current authenticated user.

    Returns:
        list[FlashcardSchema]: The list of flashcards for the learning session.
    """
    return []

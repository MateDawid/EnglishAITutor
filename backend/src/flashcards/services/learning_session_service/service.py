"""
Main service function for generating a learning session based on user ratings.
"""

from sqlalchemy.orm import with_expression

from auth.models import DbUser
from sqlalchemy import func, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from flashcards.services.learning_session_service.flashcard_limits import MAX_CARDS
from flashcards.services.learning_session_service.rating_queries import _get_rated_flashcards_selects
from flashcards.services.utils import _get_user_rating_query


async def get_learning_session_from_db(db: AsyncSession, user: DbUser) -> list[FlashcardSchema]:
    """
    Get the list of flashcards for the learning session from the database.

    Gets flashcards based on the user's ratings, prioritizing "hard" rated flashcards, followed by "medium", "easy",
    and finally flashcards that have not been rated yet. The function limits the number of flashcards returned
    for each category and orders them randomly.

    Returns:
        list[FlashcardSchema]: The list of flashcards for the learning session.
    """
    # Base query to get flashcard IDs and their corresponding user ratings
    user_rating_subquery = _get_user_rating_query(user_id=user.id)
    base_flashcard_query = select(
        DbFlashcard.id.label("id"),
        user_rating_subquery.label("rating"),
    ).subquery()

    # Create a union of queries for each rating category, limiting number of flashcards retrieved for each category
    rated_flashcards_selects = await _get_rated_flashcards_selects(db, base_flashcard_query)
    rated_flashcards_query = union_all(*rated_flashcards_selects).subquery()

    # Execute the final query to get the flashcards for the learning session, limiting total number of flashcards
    query = (
        select(DbFlashcard)
        .join(
            rated_flashcards_query,
            rated_flashcards_query.c.id == DbFlashcard.id,
        )
        .limit(MAX_CARDS)
        .order_by(func.random())
        .options(with_expression(DbFlashcard.rating, user_rating_subquery))
    )
    result = await db.execute(query)

    # Convert the result to a list of FlashcardSchema objects and return it
    return [FlashcardSchema.model_validate(flashcard, from_attributes=True) for flashcard in result.scalars().all()]

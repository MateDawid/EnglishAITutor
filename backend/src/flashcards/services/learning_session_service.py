from sqlalchemy.orm import with_expression

from auth.models import DbUser
from sqlalchemy import case, func, literal, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.enums import DatabaseRating
from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from flashcards.services.utils import _get_user_rating_query


async def get_learning_session_from_db(
    db: AsyncSession,
    user: DbUser,
) -> list[FlashcardSchema]:
    """
    Get the list of flashcards for the learning session from the database.

    Gets flashcards based on the user's ratings, prioritizing "hard" rated flashcards, followed by "medium", "easy",
    and finally flashcards that have not been rated yet. The function limits the number of flashcards returned
    for each category and orders them randomly.

    Args:
        db (AsyncSession): The database session to use for the query.
        user (DbUser): The current authenticated user.

    Returns:
        list[FlashcardSchema]: The list of flashcards for the learning session.
    """
    user_rating_subquery = _get_user_rating_query(user_id=user.id)

    flashcards_query = select(
        DbFlashcard.id.label("id"),
        user_rating_subquery.label("rating"),
    ).subquery()

    hard_query = (
        select(
            flashcards_query.c.id,
            literal(1).label("priority"),
        )
        .where(flashcards_query.c.rating == DatabaseRating.HARD)
        .order_by(func.random())
        .limit(5)
    )
    medium_query = (
        select(
            flashcards_query.c.id,
            literal(2).label("priority"),
        )
        .where(flashcards_query.c.rating == DatabaseRating.MEDIUM)
        .order_by(func.random())
        .limit(3)
    )
    easy_query = (
        select(
            flashcards_query.c.id,
            literal(3).label("priority"),
        )
        .where(flashcards_query.c.rating == DatabaseRating.EASY)
        .order_by(func.random())
        .limit(2)
    )
    not_rated_query = (
        select(
            flashcards_query.c.id,
            literal(4).label("priority"),
        )
        .where(flashcards_query.c.rating.is_(None))
        .order_by(func.random())
        .limit(10)
    )
    selected_flashcards_query = union_all(
        hard_query,
        medium_query,
        easy_query,
        not_rated_query,
    ).subquery()

    priority = case(
        (selected_flashcards_query.c.priority == 1, 1),
        (selected_flashcards_query.c.priority == 2, 2),
        (selected_flashcards_query.c.priority == 3, 3),
        else_=4,
    )

    query = (
        select(DbFlashcard)
        .join(
            selected_flashcards_query,
            selected_flashcards_query.c.id == DbFlashcard.id,
        )
        .order_by(priority)
        .limit(10)
        .options(with_expression(DbFlashcard.rating, user_rating_subquery))
    )
    result = await db.execute(query)

    return [
        FlashcardSchema.model_validate(
            flashcard,
            from_attributes=True,
        )
        for flashcard in result.scalars().all()
    ]

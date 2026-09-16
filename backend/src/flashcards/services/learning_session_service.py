from enum import IntEnum

from sqlalchemy.orm import with_expression

from auth.models import DbUser
from sqlalchemy import case, func, literal, select, union_all, Select, Subquery
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.enums import DatabaseRating
from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from flashcards.services.utils import _get_user_rating_query


class FlashcardPriority(IntEnum):
    HARD = 1
    MEDIUM = 2
    EASY = 3
    NOT_RATED = 4


class LearningSessionService:
    """
    Service class for managing learning sessions.

    This class provides methods to retrieve flashcards for a learning session based on user ratings.
    It prioritizes flashcards that are rated as "hard" by the user, followed by "medium", "easy", and finally
    flashcards that have not been rated yet. The number of flashcards returned for each category is limited
    to ensure a balanced learning session.
    """

    HARD_CARDS_LIMIT = 5
    MEDIUM_CARDS_LIMIT = 3
    EASY_CARDS_LIMIT = 2
    ALL_CARDS_LIMIT = HARD_CARDS_LIMIT + MEDIUM_CARDS_LIMIT + EASY_CARDS_LIMIT

    def __init__(self, db: AsyncSession, user: DbUser):
        """
        Initialize the LearningSessionService with a database session and the current authenticated user.

        Args:
            db (AsyncSession): The database session to use for queries.
            user (DbUser): The current authenticated user.
        """
        self.db = db
        self.user = user
        self._base_flashcard_query = None

    async def get_learning_session_from_db(self) -> list[FlashcardSchema]:
        """
        Get the list of flashcards for the learning session from the database.

        Gets flashcards based on the user's ratings, prioritizing "hard" rated flashcards, followed by "medium", "easy",
        and finally flashcards that have not been rated yet. The function limits the number of flashcards returned
        for each category and orders them randomly.

        Returns:
            list[FlashcardSchema]: The list of flashcards for the learning session.
        """
        user_rating_subquery = _get_user_rating_query(user_id=self.user.id)
        base_flashcard_query = select(
            DbFlashcard.id.label("id"),
            user_rating_subquery.label("rating"),
        ).subquery()
        rated_flashcards_query = union_all(
            self._get_hard_flashcards_query(base_flashcard_query),
            self._get_medium_flashcards_query(base_flashcard_query),
            self._get_easy_flashcards_query(base_flashcard_query),
            self._get_not_rated_flashcards_query(base_flashcard_query),
        ).subquery()

        priority = case(
            (rated_flashcards_query.c.priority == FlashcardPriority.HARD.value, FlashcardPriority.HARD.value),
            (rated_flashcards_query.c.priority == FlashcardPriority.MEDIUM.value, FlashcardPriority.MEDIUM.value),
            (rated_flashcards_query.c.priority == FlashcardPriority.EASY.value, FlashcardPriority.EASY.value),
            else_=FlashcardPriority.NOT_RATED.value,
        )

        query = (
            select(DbFlashcard)
            .join(
                rated_flashcards_query,
                rated_flashcards_query.c.id == DbFlashcard.id,
            )
            .order_by(priority)
            .limit(self.ALL_CARDS_LIMIT)
            .options(with_expression(DbFlashcard.rating, user_rating_subquery))
        )
        result = await self.db.execute(query)

        return [
            FlashcardSchema.model_validate(
                flashcard,
                from_attributes=True,
            )
            for flashcard in result.scalars().all()
        ]

    def _get_hard_flashcards_query(self, flashcards_query: Subquery) -> Select:
        """
        Get the database query for "hard" rated flashcards.

        Args:
            flashcards_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

        Returns:
            Select: The database query for "hard" rated flashcards.
        """
        return (
            select(
                flashcards_query.c.id,
                literal(FlashcardPriority.HARD.value).label("priority"),
            )
            .where(flashcards_query.c.rating == DatabaseRating.HARD)
            .order_by(func.random())
            .limit(self.HARD_CARDS_LIMIT)
        )

    def _get_medium_flashcards_query(self, flashcards_query: Subquery) -> Select:
        """
        Get the database query for "medium" rated flashcards.

        Args:
            flashcards_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

        Returns:
            Select: The database query for "medium" rated flashcards.
        """
        return (
            select(
                flashcards_query.c.id,
                literal(FlashcardPriority.MEDIUM.value).label("priority"),
            )
            .where(flashcards_query.c.rating == DatabaseRating.MEDIUM)
            .order_by(func.random())
            .limit(self.MEDIUM_CARDS_LIMIT)
        )

    def _get_easy_flashcards_query(self, flashcards_query: Subquery) -> Select:
        """
        Get the database query for "easy" rated flashcards.

        Args:
            flashcards_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

        Returns:
            Select: The database query for "easy" rated flashcards.
        """
        return (
            select(
                flashcards_query.c.id,
                literal(FlashcardPriority.EASY.value).label("priority"),
            )
            .where(flashcards_query.c.rating == DatabaseRating.EASY)
            .order_by(func.random())
            .limit(self.EASY_CARDS_LIMIT)
        )

    def _get_not_rated_flashcards_query(self, flashcards_query: Subquery) -> Select:
        """
        Get the database query for not rated flashcards.

        Args:
            flashcards_query (Subquery): The subquery containing flashcard IDs and their corresponding user ratings.

        Returns:
            Select: The database query for not rated flashcards.
        """

        return (
            select(
                flashcards_query.c.id,
                literal(FlashcardPriority.NOT_RATED.value).label("priority"),
            )
            .where(flashcards_query.c.rating.is_(None))
            .order_by(func.random())
            .limit(self.ALL_CARDS_LIMIT)
        )

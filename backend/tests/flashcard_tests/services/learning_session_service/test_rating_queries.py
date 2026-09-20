import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from factories.flashcard import FlashcardFactory
from factories.user_rating import UserRatingFactory
from flashcards.enums import DatabaseRating
from flashcards.models import DbFlashcard
from flashcards.services.learning_session_service.rating_queries import (
    _get_rated_flashcards_query,
    _get_rated_flashcards_selects,
    _get_rating_query_limits,
    _get_ratings_count,
)
from flashcards.services.utils import _get_user_rating_query


async def _seed_learning_session_cards(
    db_session: AsyncSession,
    test_user: DbUser,
    hard_count: int,
    medium_count: int,
    easy_count: int,
    unrated_count: int,
) -> None:
    FlashcardFactory._meta.sqlalchemy_session = db_session
    hard_cards = [FlashcardFactory.build(word=f"hard_{i}") for i in range(hard_count)]
    medium_cards = [FlashcardFactory.build(word=f"medium_{i}") for i in range(medium_count)]
    easy_cards = [FlashcardFactory.build(word=f"easy_{i}") for i in range(easy_count)]
    unrated_cards = [FlashcardFactory.build(word=f"unrated_{i}") for i in range(unrated_count)]
    db_session.add_all(hard_cards + medium_cards + easy_cards + unrated_cards)
    await db_session.flush()

    UserRatingFactory._meta.sqlalchemy_session = db_session
    db_session.add_all(
        [
            *[
                UserRatingFactory.build(
                    user_id=test_user.id,
                    flashcard_id=flashcard.id,
                    rating=DatabaseRating.HARD,
                )
                for flashcard in hard_cards
            ],
            *[
                UserRatingFactory.build(
                    user_id=test_user.id,
                    flashcard_id=flashcard.id,
                    rating=DatabaseRating.MEDIUM,
                )
                for flashcard in medium_cards
            ],
            *[
                UserRatingFactory.build(
                    user_id=test_user.id,
                    flashcard_id=flashcard.id,
                    rating=DatabaseRating.EASY,
                )
                for flashcard in easy_cards
            ],
        ]
    )
    await db_session.flush()


def _get_base_flashcard_query(user_id):
    user_rating_subquery = _get_user_rating_query(user_id=user_id)
    return select(
        DbFlashcard.id.label("id"),
        user_rating_subquery.label("rating"),
    ).subquery()


@pytest.mark.asyncio
async def test_get_ratings_count_returns_all_rating_buckets(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: Rated and unrated flashcards for a user.
    WHEN: Ratings count is queried for learning-session selection.
    THEN: Counts are returned for hard, medium, easy, and unrated buckets.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=2,
        medium_count=1,
        easy_count=0,
        unrated_count=3,
    )
    base_flashcard_query = _get_base_flashcard_query(test_user.id)

    ratings_count = await _get_ratings_count(db_session, base_flashcard_query)

    assert ratings_count[DatabaseRating.HARD] == 2
    assert ratings_count[DatabaseRating.MEDIUM] == 1
    assert ratings_count[DatabaseRating.EASY] == 0
    assert ratings_count[None] == 3


@pytest.mark.asyncio
async def test_get_rating_query_limits_caps_each_bucket(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: More rated flashcards than allowed by rating bucket limits.
    WHEN: Query limits are calculated for learning-session selection.
    THEN: Hard, medium, and easy limits are capped and unrated gets remaining capacity.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=8,
        medium_count=5,
        easy_count=4,
        unrated_count=3,
    )
    base_flashcard_query = _get_base_flashcard_query(test_user.id)

    rating_query_limits = await _get_rating_query_limits(db_session, base_flashcard_query)

    assert rating_query_limits[DatabaseRating.HARD] == 5
    assert rating_query_limits[DatabaseRating.MEDIUM] == 3
    assert rating_query_limits[DatabaseRating.EASY] == 2
    assert rating_query_limits[None] == 0


@pytest.mark.asyncio
async def test_get_rated_flashcards_selects_skips_zero_limit_buckets(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: Easy-rated flashcards are missing while other buckets have available cards.
    WHEN: Rated flashcard select queries are created.
    THEN: Buckets with zero limits are skipped and non-empty bucket selects are returned.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=2,
        medium_count=1,
        easy_count=0,
        unrated_count=5,
    )
    base_flashcard_query = _get_base_flashcard_query(test_user.id)

    selects = await _get_rated_flashcards_selects(db_session, base_flashcard_query)

    assert len(selects) == 3
    selected_counts = []
    for query in selects:
        result = await db_session.execute(query)
        selected_counts.append(len(result.all()))
    assert selected_counts == [1, 2, 5]


@pytest.mark.asyncio
async def test_get_rated_flashcards_query_returns_none_for_zero_limit(
    test_user: DbUser,
):
    """
    GIVEN: A rating bucket configured with zero selection limit.
    WHEN: The bucket query is built.
    THEN: No select query is returned.
    """
    base_flashcard_query = _get_base_flashcard_query(test_user.id)

    query = _get_rated_flashcards_query(
        base_flashcard_query,
        DatabaseRating.HARD,
        {
            DatabaseRating.HARD: 0,
            DatabaseRating.MEDIUM: 0,
            DatabaseRating.EASY: 0,
            None: 0,
        },
    )

    assert query is None


@pytest.mark.asyncio
async def test_get_rated_flashcards_query_raises_for_unknown_rating_key(
    test_user: DbUser,
):
    """
    GIVEN: A rating limits mapping missing the requested rating key.
    WHEN: A query is built for the missing rating key.
    THEN: ValueError is raised.
    """
    base_flashcard_query = _get_base_flashcard_query(test_user.id)

    with pytest.raises(ValueError):
        _get_rated_flashcards_query(
            base_flashcard_query,
            DatabaseRating.MEDIUM,
            {
                DatabaseRating.HARD: 1,
                None: 0,
            },
        )

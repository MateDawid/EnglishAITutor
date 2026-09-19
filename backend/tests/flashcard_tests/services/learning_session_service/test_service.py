import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from factories.flashcard import FlashcardFactory
from factories.user_rating import UserRatingFactory
from flashcards.enums import DatabaseRating
from flashcards.services.learning_session_service.flashcard_limits import MAX_CARDS
from flashcards.services.learning_session_service.service import get_learning_session_from_db


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


@pytest.mark.asyncio
async def test_get_learning_session_from_db_applies_rating_bucket_limits(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: More flashcards than each learning-session rating bucket can include.
    WHEN: Learning session flashcards are requested.
    THEN: The returned set is capped by hard/medium/easy limits up to MAX_CARDS.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=8,
        medium_count=5,
        easy_count=4,
        unrated_count=3,
    )

    flashcards = await get_learning_session_from_db(db=db_session, user=test_user)

    assert len(flashcards) == MAX_CARDS
    assert sum(card.rating == DatabaseRating.HARD for card in flashcards) == 5
    assert sum(card.rating == DatabaseRating.MEDIUM for card in flashcards) == 3
    assert sum(card.rating == DatabaseRating.EASY for card in flashcards) == 2
    assert sum(card.rating is None for card in flashcards) == 0


@pytest.mark.asyncio
async def test_get_learning_session_from_db_fills_with_unrated_cards(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: Not enough rated flashcards to reach MAX_CARDS.
    WHEN: Learning session flashcards are requested.
    THEN: Remaining slots are filled with unrated flashcards.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=2,
        medium_count=1,
        easy_count=0,
        unrated_count=10,
    )

    flashcards = await get_learning_session_from_db(db=db_session, user=test_user)

    assert len(flashcards) == MAX_CARDS
    assert sum(card.rating == DatabaseRating.HARD for card in flashcards) == 2
    assert sum(card.rating == DatabaseRating.MEDIUM for card in flashcards) == 1
    assert sum(card.rating == DatabaseRating.EASY for card in flashcards) == 0
    assert sum(card.rating is None for card in flashcards) == 7


@pytest.mark.asyncio
async def test_get_learning_session_from_db_keeps_hard_cards_capped_without_unrated(
    test_user: DbUser,
    db_session: AsyncSession,
):
    """
    GIVEN: Only hard-rated flashcards are available.
    WHEN: Learning session flashcards are requested.
    THEN: Returned flashcards are capped to the hard-rated bucket limit.
    """
    await _seed_learning_session_cards(
        db_session=db_session,
        test_user=test_user,
        hard_count=12,
        medium_count=0,
        easy_count=0,
        unrated_count=0,
    )

    flashcards = await get_learning_session_from_db(db=db_session, user=test_user)

    assert len(flashcards) == 5
    assert sum(card.rating == DatabaseRating.HARD for card in flashcards) == 5
    assert sum(card.rating is None for card in flashcards) == 0

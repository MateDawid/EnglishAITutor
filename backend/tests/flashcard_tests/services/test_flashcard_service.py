import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from factories.user import UserFactory
from flashcards.enums import DatabaseRating, RatingFilter
from flashcards.models import DbUserRating
from flashcards.models.db_flashcard import PartOfSpeech
from flashcards.schemas import FlashcardSchema
from flashcards.services.flashcard_service import get_flashcards_from_db, update_or_create_user_rating
from utils.pagination.schemas import PaginationQuery, PaginatedResponse
from factories.flashcard import FlashcardFactory
from factories.user_rating import UserRatingFactory


@pytest.mark.asyncio
class TestGetFlashcardsFromDbFunction:
    """
    Tests for get_flashcards_from_db function.
    """

    async def test_get_flashcards_from_db_returns_paginated_response(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are requested with pagination.
        THEN: A paginated response is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(15):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={},
        )

        assert isinstance(response, PaginatedResponse)
        assert len(response.items) == 10
        assert response.total == 15
        assert response.page == 1
        assert response.page_size == 10
        assert response.total_pages == 2
        assert response.has_next is True
        assert response.has_previous is False

    async def test_get_flashcards_from_db_returns_correct_schema(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Flashcards in the database.
        WHEN: Flashcards are requested.
        THEN: Items are returned as FlashcardSchema instances.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build(
            word="test",
            meaning="test meaning",
            part_of_speech=PartOfSpeech.NOUN,
            example="This is a test.",
        )
        db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={},
        )

        assert len(response.items) == 1
        item = response.items[0]
        assert isinstance(item, FlashcardSchema)
        assert item.word == "test"
        assert item.meaning == "test meaning"
        assert item.part_of_speech == PartOfSpeech.NOUN
        assert item.example == "This is a test."
        assert item.user_rating is None

    async def test_get_flashcards_from_db_with_empty_database(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No flashcards in the database.
        WHEN: Flashcards are requested.
        THEN: An empty paginated response is returned.
        """
        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={},
        )

        assert isinstance(response, PaginatedResponse)
        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_previous is False

    async def test_get_flashcards_from_db_with_ordering(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are requested with ordering.
        THEN: Flashcards are returned in correct order.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="zebra")
        flashcard2 = FlashcardFactory.build(word="apple")
        flashcard3 = FlashcardFactory.build(word="mango")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by="word",
            filters={},
        )

        assert len(response.items) == 3
        assert response.items[0].word == "apple"
        assert response.items[1].word == "mango"
        assert response.items[2].word == "zebra"

    async def test_get_flashcards_from_db_with_descending_ordering(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are requested with descending ordering.
        THEN: Flashcards are returned in reverse order.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="apple")
        flashcard2 = FlashcardFactory.build(word="banana")
        flashcard3 = FlashcardFactory.build(word="cherry")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by="-word",
            filters={},
        )

        assert len(response.items) == 3
        assert response.items[0].word == "cherry"
        assert response.items[1].word == "banana"
        assert response.items[2].word == "apple"

    async def test_get_flashcards_from_db_with_word_filter(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are filtered by word.
        THEN: Only matching flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test")
        flashcard2 = FlashcardFactory.build(word="testing")
        flashcard3 = FlashcardFactory.build(word="example")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"word": "test"},
        )

        assert len(response.items) == 2
        assert all("test" in item.word for item in response.items)

    async def test_get_flashcards_from_db_with_meaning_filter(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are filtered by meaning.
        THEN: Only matching flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(meaning="a testing word")
        flashcard2 = FlashcardFactory.build(meaning="another test")
        flashcard3 = FlashcardFactory.build(meaning="different meaning")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"meaning": "test"},
        )

        assert len(response.items) == 2
        assert all("test" in item.meaning for item in response.items)

    async def test_get_flashcards_from_db_with_multiple_filters(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are filtered by multiple fields.
        THEN: Only flashcards matching all filters are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test", meaning="a test word")
        flashcard2 = FlashcardFactory.build(word="test", meaning="different")
        flashcard3 = FlashcardFactory.build(word="other", meaning="test word")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"word": "test", "meaning": "test"},
        )

        assert len(response.items) == 1
        assert response.items[0].word == "test"
        assert "test" in response.items[0].meaning

    async def test_get_flashcards_from_db_with_ordering_and_filtering(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are filtered and ordered.
        THEN: Filtered and ordered flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test_zebra")
        flashcard2 = FlashcardFactory.build(word="test_apple")
        flashcard3 = FlashcardFactory.build(word="example")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by="word",
            filters={"word": "test"},
        )

        assert len(response.items) == 2
        assert response.items[0].word == "test_apple"
        assert response.items[1].word == "test_zebra"

    async def test_get_flashcards_from_db_with_rating_filter(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Flashcards with different ratings in the database.
        WHEN: Flashcards are filtered by rating.
        THEN: Only flashcards matching the rating filter are returned.
        """
        # Create flashcards and another user
        UserFactory._meta.sqlalchemy_session = db_session
        FlashcardFactory._meta.sqlalchemy_session = db_session
        other_user = UserFactory.build()
        easy_flashcard = FlashcardFactory.build(word="easy_word")
        hard_flashcard = FlashcardFactory.build(word="hard_word")
        unrated_flashcard = FlashcardFactory.build(word="unrated_word")
        db_session.add_all([other_user, easy_flashcard, hard_flashcard, unrated_flashcard])
        await db_session.flush()
        UserRatingFactory._meta.sqlalchemy_session = db_session
        # Create ratings for the test_user and another user
        db_session.add_all(
            [
                # User's ratings
                UserRatingFactory.build(
                    user_id=test_user.id,
                    flashcard_id=easy_flashcard.id,
                    rating=DatabaseRating.EASY,
                ),
                UserRatingFactory.build(
                    user_id=test_user.id,
                    flashcard_id=hard_flashcard.id,
                    rating=DatabaseRating.HARD,
                ),
                # Other user's ratings should not affect the test_user's filtered results
                UserRatingFactory.build(
                    user_id=other_user.id,
                    flashcard_id=easy_flashcard.id,
                    rating=DatabaseRating.MEDIUM,
                ),
                UserRatingFactory.build(
                    user_id=other_user.id,
                    flashcard_id=unrated_flashcard.id,
                    rating=DatabaseRating.EASY,
                ),
            ]
        )
        await db_session.flush()

        # Test filtering by EASY rating and NOT_RATED rating
        pagination_query = PaginationQuery(page=1, page_size=10)
        easy_response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"rating": RatingFilter.EASY},
        )
        unrated_response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"rating": RatingFilter.NOT_RATED},
        )

        assert len(easy_response.items) == 1
        assert easy_response.items[0].word == "easy_word"
        assert easy_response.items[0].user_rating == DatabaseRating.EASY
        assert len(unrated_response.items) == 1
        assert unrated_response.items[0].word == "unrated_word"
        assert unrated_response.items[0].user_rating is None

    @pytest.mark.parametrize(
        "total_items,page,page_size,expected_count",
        [
            (50, 1, 10, 10),
            (50, 5, 10, 10),
            (50, 6, 10, 0),
            (15, 1, 20, 15),
            (100, 10, 10, 10),
        ],
    )
    async def test_get_flashcards_from_db_parametrized(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
        total_items: int,
        page: int,
        page_size: int,
        expected_count: int,
    ):
        """
        GIVEN: Different combinations of total items and pagination parameters.
        WHEN: Flashcards are requested.
        THEN: The correct number of items is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(total_items):
            flashcard = FlashcardFactory.build(word=f"word_{i:03d}")
            db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=page, page_size=page_size)
        response = await get_flashcards_from_db(
            user=test_user,
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={},
        )

        assert len(response.items) == expected_count
        assert response.total == total_items


@pytest.mark.asyncio
class TestUpdateOrCreateUserRating:
    async def test_update_or_create_user_rating_creates_new_rating(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A user and a flashcard without an existing rating.
        WHEN: The user rates the flashcard.
        THEN: A new rating is created in the database.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build()
        db_session.add(flashcard)
        await db_session.flush()

        response = await update_or_create_user_rating(
            db=db_session,
            user_id=test_user.id,
            flashcard_id=flashcard.id,
            rating=DatabaseRating.EASY,
        )
        db_result = await db_session.execute(
            select(DbUserRating).where(
                DbUserRating.user_id == test_user.id,
                DbUserRating.flashcard_id == flashcard.id,
            )
        )
        user_rating = db_result.scalar_one()

        assert response.rating_changed is True
        assert user_rating.rating == DatabaseRating.EASY

    async def test_update_or_create_user_rating_returns_false_for_same_rating(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A user and a flashcard with an existing rating.
        WHEN: The user rates the flashcard with the same rating.
        THEN: The function returns that the rating has not changed.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build()
        db_session.add(flashcard)
        await db_session.flush()
        UserRatingFactory._meta.sqlalchemy_session = db_session
        db_session.add(
            UserRatingFactory.build(
                user_id=test_user.id,
                flashcard_id=flashcard.id,
                rating=DatabaseRating.MEDIUM,
            )
        )
        await db_session.flush()

        response = await update_or_create_user_rating(
            db=db_session,
            user_id=test_user.id,
            flashcard_id=flashcard.id,
            rating=DatabaseRating.MEDIUM,
        )

        assert response.rating_changed is False

    async def test_update_or_create_user_rating_updates_existing_rating(
        self,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A user and a flashcard with an existing rating.
        WHEN: The user rates the flashcard with a different rating.
        THEN: The existing rating is updated in the database.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build()
        db_session.add(flashcard)
        await db_session.flush()
        UserRatingFactory._meta.sqlalchemy_session = db_session
        db_session.add(
            UserRatingFactory.build(
                user_id=test_user.id,
                flashcard_id=flashcard.id,
                rating=DatabaseRating.HARD,
            )
        )
        await db_session.flush()

        response = await update_or_create_user_rating(
            db=db_session,
            user_id=test_user.id,
            flashcard_id=flashcard.id,
            rating=DatabaseRating.EASY,
        )
        db_result = await db_session.execute(
            select(DbUserRating).where(
                DbUserRating.user_id == test_user.id,
                DbUserRating.flashcard_id == flashcard.id,
            )
        )
        user_rating = db_result.scalar_one()

        assert response.rating_changed is True
        assert user_rating.rating == DatabaseRating.EASY

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.db_flashcard import PartOfSpeech
from flashcards.schemas import FlashcardSchema
from flashcards.services.flashcard_service import get_flashcards_from_db
from utils.pagination.schemas import PaginationQuery, PaginatedResponse
from factories.flashcard import FlashcardFactory


@pytest.mark.asyncio
class TestGetFlashcardsFromDbFunction:
    """
    Tests for get_flashcards_from_db function.
    """

    async def test_get_flashcards_from_db_returns_paginated_response(
        self,
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

    async def test_get_flashcards_from_db_with_empty_database(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No flashcards in the database.
        WHEN: Flashcards are requested.
        THEN: An empty paginated response is returned.
        """
        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_flashcards_from_db(
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
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"word": "test"},
        )

        assert len(response.items) == 2
        assert all("test" in item.word for item in response.items)

    async def test_get_flashcards_from_db_with_meaning_filter(
        self,
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
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={"meaning": "test"},
        )

        assert len(response.items) == 2
        assert all("test" in item.meaning for item in response.items)

    async def test_get_flashcards_from_db_with_multiple_filters(
        self,
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
            db=db_session,
            pagination_query=pagination_query,
            order_by="word",
            filters={"word": "test"},
        )

        assert len(response.items) == 2
        assert response.items[0].word == "test_apple"
        assert response.items[1].word == "test_zebra"

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
            db=db_session,
            pagination_query=pagination_query,
            order_by=None,
            filters={},
        )

        assert len(response.items) == expected_count
        assert response.total == total_items

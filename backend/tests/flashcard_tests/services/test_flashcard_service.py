import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.db_flashcard import PartOfSpeech
from flashcards.schemas import FlashcardSchema
from flashcards.services.flashcard_service import get_flashcards_from_db
from pagination.schemas import PaginationQuery, PaginatedResponse
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
        response = await get_flashcards_from_db(db_session, pagination_query)

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
        response = await get_flashcards_from_db(db_session, pagination_query)

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
        response = await get_flashcards_from_db(db_session, pagination_query)

        assert isinstance(response, PaginatedResponse)
        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_previous is False

    async def test_get_flashcards_from_db_second_page(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: The second page is requested.
        THEN: The correct page is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(25):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=2, page_size=10)
        response = await get_flashcards_from_db(db_session, pagination_query)

        assert len(response.items) == 10
        assert response.total == 25
        assert response.page == 2
        assert response.has_next is True
        assert response.has_previous is True

    async def test_get_flashcards_from_db_last_page(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: The last page is requested.
        THEN: The remaining items are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(23):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=3, page_size=10)
        response = await get_flashcards_from_db(db_session, pagination_query)

        assert len(response.items) == 3
        assert response.total == 23
        assert response.page == 3
        assert response.has_next is False
        assert response.has_previous is True

    async def test_get_flashcards_from_db_with_custom_page_size(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: Flashcards are requested with a custom page size.
        THEN: The correct number of items is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(30):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        pagination_query = PaginationQuery(page=1, page_size=5)
        response = await get_flashcards_from_db(db_session, pagination_query)

        assert len(response.items) == 5
        assert response.total == 30
        assert response.page_size == 5
        assert response.total_pages == 6

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
        response = await get_flashcards_from_db(db_session, pagination_query)

        assert len(response.items) == expected_count
        assert response.total == total_items

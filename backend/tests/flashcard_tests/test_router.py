import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models.db_flashcard import PartOfSpeech
from factories.flashcard import FlashcardFactory


@pytest.mark.asyncio
class TestFlashcardListView:
    """
    Tests for GET /flashcards/ endpoint.
    """

    async def test_flashcard_list_view_returns_paginated_response(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with authentication.
        THEN: A paginated response is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(15):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        response = await authenticated_client.get(
            "/flashcards/",
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1

    async def test_flashcard_list_view_requires_authentication(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A request without authentication.
        WHEN: GET /flashcards/ is called.
        THEN: 401 Unauthorized is returned.
        """
        response = await client.get("/flashcards/")

        assert response.status_code == 401

    async def test_flashcard_list_view_with_pagination_params(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with pagination parameters.
        THEN: The correct page is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        for i in range(25):
            flashcard = FlashcardFactory.build(word=f"word_{i:02d}")
            db_session.add(flashcard)
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?page=2&page_size=10")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 10
        assert len(data["items"]) == 10
        assert data["total"] == 25

    async def test_flashcard_list_view_with_ordering(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with order_by parameter.
        THEN: Flashcards are returned in correct order.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="zebra")
        flashcard2 = FlashcardFactory.build(word="apple")
        flashcard3 = FlashcardFactory.build(word="mango")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?order_by=word")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["items"][0]["word"] == "apple"
        assert data["items"][1]["word"] == "mango"
        assert data["items"][2]["word"] == "zebra"

    async def test_flashcard_list_view_with_descending_ordering(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with descending order_by.
        THEN: Flashcards are returned in reverse order.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="apple")
        flashcard2 = FlashcardFactory.build(word="banana")
        flashcard3 = FlashcardFactory.build(word="cherry")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?order_by=-word")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["items"][0]["word"] == "cherry"
        assert data["items"][1]["word"] == "banana"
        assert data["items"][2]["word"] == "apple"

    async def test_flashcard_list_view_with_word_filter(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with word filter.
        THEN: Only matching flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test")
        flashcard2 = FlashcardFactory.build(word="testing")
        flashcard3 = FlashcardFactory.build(word="example")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?word=test")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert all("test" in item["word"] for item in data["items"])

    async def test_flashcard_list_view_with_meaning_filter(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with meaning filter.
        THEN: Only matching flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(meaning="a test word")
        flashcard2 = FlashcardFactory.build(meaning="another test")
        flashcard3 = FlashcardFactory.build(meaning="different meaning")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?meaning=test")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert all("test" in item["meaning"] for item in data["items"])

    async def test_flashcard_list_view_with_multiple_filters(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with multiple filters.
        THEN: Only flashcards matching all filters are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test", meaning="a test word")
        flashcard2 = FlashcardFactory.build(word="test", meaning="different")
        flashcard3 = FlashcardFactory.build(word="other", meaning="test word")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?word=test&meaning=test")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["word"] == "test"
        assert "test" in data["items"][0]["meaning"]

    async def test_flashcard_list_view_with_exact_match_filter(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with exact match filter.
        THEN: Only exact matching flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test")
        flashcard2 = FlashcardFactory.build(word="test value")
        flashcard3 = FlashcardFactory.build(word="testing")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get(
            '/flashcards/?word="test"',
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["word"] == "test"

    async def test_flashcard_list_view_empty_result(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No flashcards in the database.
        WHEN: GET /flashcards/ is called.
        THEN: An empty result is returned.
        """
        response = await authenticated_client.get(
            "/flashcards/",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["total_pages"] == 0

    async def test_flashcard_list_view_returns_correct_schema(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A flashcard in the database.
        WHEN: GET /flashcards/ is called.
        THEN: The correct schema fields are returned.
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

        response = await authenticated_client.get(
            "/flashcards/",
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        item = data["items"][0]
        assert "id" in item
        assert item["word"] == "test"
        assert item["meaning"] == "test meaning"
        assert item["part_of_speech"] == PartOfSpeech.NOUN
        assert item["example"] == "This is a test."

    async def test_flashcard_list_view_with_combined_ordering_and_filtering(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple flashcards in the database.
        WHEN: GET /flashcards/ is called with both ordering and filtering.
        THEN: Filtered and ordered flashcards are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard1 = FlashcardFactory.build(word="test_zebra")
        flashcard2 = FlashcardFactory.build(word="test_apple")
        flashcard3 = FlashcardFactory.build(word="example")
        db_session.add_all([flashcard1, flashcard2, flashcard3])
        await db_session.flush()

        response = await authenticated_client.get(
            "/flashcards/?word=test&order_by=word",
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["word"] == "test_apple"
        assert data["items"][1]["word"] == "test_zebra"

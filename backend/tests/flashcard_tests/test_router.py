import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import DbUser
from flashcards.enums import DatabaseRating
from flashcards.models import DbUserRating
from flashcards.models.db_flashcard import PartOfSpeech
from factories.flashcard import FlashcardFactory
from factories.user_rating import UserRatingFactory


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
        assert item["rating"] is None

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

    async def test_flashcard_list_view_with_part_of_speech_filter(
        self,
        authenticated_client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Flashcards with different parts of speech in the database.
        WHEN: GET /flashcards/ is called with part_of_speech filter.
        THEN: Only flashcards matching the specified part of speech are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        noun_flashcard = FlashcardFactory.build(word="cat", part_of_speech=PartOfSpeech.NOUN)
        verb_flashcard = FlashcardFactory.build(word="run", part_of_speech=PartOfSpeech.VERB)
        db_session.add_all([noun_flashcard, verb_flashcard])
        await db_session.flush()

        response = await authenticated_client.get("/flashcards/?part_of_speech=noun")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["word"] == "cat"
        assert data["items"][0]["part_of_speech"] == PartOfSpeech.NOUN

    async def test_flashcard_list_view_with_rating_filter(
        self,
        authenticated_client: AsyncClient,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Flashcards with different ratings in the database.
        WHEN: GET /flashcards/ is called with rating filter.
        THEN: Only flashcards matching the specified rating are returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        easy_flashcard = FlashcardFactory.build(word="easy_word")
        hard_flashcard = FlashcardFactory.build(word="hard_word")
        unrated_flashcard = FlashcardFactory.build(word="unrated_word")
        db_session.add_all([easy_flashcard, hard_flashcard, unrated_flashcard])
        await db_session.flush()
        UserRatingFactory._meta.sqlalchemy_session = db_session
        db_session.add_all(
            [
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
            ]
        )
        await db_session.flush()

        easy_response = await authenticated_client.get("/flashcards/?rating=1")
        not_rated_response = await authenticated_client.get("/flashcards/?rating=0")

        assert easy_response.status_code == 200
        easy_data = easy_response.json()
        assert len(easy_data["items"]) == 1
        assert easy_data["items"][0]["word"] == "easy_word"
        assert easy_data["items"][0]["rating"] == DatabaseRating.EASY
        assert not_rated_response.status_code == 200
        not_rated_data = not_rated_response.json()
        assert len(not_rated_data["items"]) == 1
        assert not_rated_data["items"][0]["word"] == "unrated_word"
        assert not_rated_data["items"][0]["rating"] is None


@pytest.mark.asyncio
class TestRateFlashcardView:
    async def test_rate_flashcard_requires_authentication(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A request without authentication.
        WHEN: POST /flashcards/{flashcard_id} is called.
        THEN: 401 Unauthorized is returned.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build()
        db_session.add(flashcard)
        await db_session.flush()

        response = await client.post(f"/flashcards/{flashcard.id}", json={"rating": DatabaseRating.EASY})

        assert response.status_code == 401

    async def test_rate_flashcard_creates_new_rating(
        self,
        authenticated_client: AsyncClient,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A flashcard without a user rating in the database.
        WHEN: POST /flashcards/{flashcard_id} is called with a rating.
        THEN: A new user rating is created in the database.
        """
        FlashcardFactory._meta.sqlalchemy_session = db_session
        flashcard = FlashcardFactory.build()
        db_session.add(flashcard)
        await db_session.flush()

        response = await authenticated_client.post(
            f"/flashcards/{flashcard.id}",
            json={"rating": DatabaseRating.EASY},
        )
        db_result = await db_session.execute(
            select(DbUserRating).where(
                DbUserRating.user_id == test_user.id,
                DbUserRating.flashcard_id == flashcard.id,
            )
        )
        user_rating = db_result.scalar_one()

        assert response.status_code == 201
        assert response.json() == {"rating_changed": True}
        assert user_rating.rating == DatabaseRating.EASY

    async def test_rate_flashcard_returns_false_for_same_rating(
        self,
        authenticated_client: AsyncClient,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A flashcard with an existing user rating in the database.
        WHEN: POST /flashcards/{flashcard_id} is called with the same rating.
        THEN: The response indicates that the rating has not changed.
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

        response = await authenticated_client.post(
            f"/flashcards/{flashcard.id}",
            json={"rating": DatabaseRating.MEDIUM},
        )

        assert response.status_code == 201
        assert response.json() == {"rating_changed": False}

    async def test_rate_flashcard_updates_existing_rating(
        self,
        authenticated_client: AsyncClient,
        test_user: DbUser,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A flashcard with an existing user rating in the database.
        WHEN: POST /flashcards/{flashcard_id} is called with a different rating.
        THEN: The existing user rating is updated in the database.
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

        response = await authenticated_client.post(
            f"/flashcards/{flashcard.id}",
            json={"rating": DatabaseRating.EASY},
        )
        db_result = await db_session.execute(
            select(DbUserRating).where(
                DbUserRating.user_id == test_user.id,
                DbUserRating.flashcard_id == flashcard.id,
            )
        )
        user_rating = db_result.scalar_one()

        assert response.status_code == 201
        assert response.json() == {"rating_changed": True}
        assert user_rating.rating == DatabaseRating.EASY

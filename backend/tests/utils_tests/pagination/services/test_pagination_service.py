import uuid
import pytest
from pydantic import BaseModel
from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from utils.database import Base
from utils.pagination.schemas import PaginationQuery, PaginatedResponse
from utils.pagination.services.pagination_service import _get_total_count, _get_items, get_paginated_response


class DbTestItem(Base):
    """
    Generic test model for pagination testing.
    """

    __tablename__ = "test_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)


class TestItemSchema(BaseModel):
    """
    Generic test schema for pagination testing.
    """

    id: uuid.UUID
    name: str
    category: str


@pytest.mark.asyncio
class TestGetTotalCountFunction:
    """
    Tests for _get_total_count function.
    """

    async def test_get_total_count_with_multiple_items(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Total count is requested.
        THEN: The correct count is returned.
        """
        for i in range(5):
            item = DbTestItem(name=f"item_{i}", category="test")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem)
        total = await _get_total_count(db_session, query)

        assert total == 5

    async def test_get_total_count_with_no_items(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No items in the database.
        WHEN: Total count is requested.
        THEN: Zero is returned.
        """
        query = select(DbTestItem)
        total = await _get_total_count(db_session, query)

        assert total == 0

    async def test_get_total_count_with_filtered_query(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different categories.
        WHEN: Total count is requested with a filter.
        THEN: Only matching items are counted.
        """
        item1 = DbTestItem(name="item_1", category="alpha")
        item2 = DbTestItem(name="item_2", category="beta")
        item3 = DbTestItem(name="item_3", category="alpha")
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem).where(DbTestItem.category == "alpha")
        total = await _get_total_count(db_session, query)

        assert total == 2


@pytest.mark.asyncio
class TestGetItemsFunction:
    """
    Tests for _get_items function.
    """

    async def test_get_items_with_pagination(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are requested with pagination.
        THEN: The correct items are returned.
        """
        for i in range(10):
            item = DbTestItem(name=f"item_{i}", category="test")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem).order_by(DbTestItem.name)
        pagination_query = PaginationQuery(page=1, page_size=5)
        items = await _get_items(db_session, query, TestItemSchema, pagination_query)

        assert len(items) == 5
        assert all(isinstance(item, TestItemSchema) for item in items)

    async def test_get_items_with_offset(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are requested with an offset.
        THEN: Items from the correct page are returned.
        """
        for i in range(10):
            item = DbTestItem(name=f"item_{i:02d}", category="test")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem).order_by(DbTestItem.name)
        pagination_query = PaginationQuery(page=2, page_size=5)
        items = await _get_items(db_session, query, TestItemSchema, pagination_query)

        assert len(items) == 5
        assert items[0].name == "item_05"
        assert items[1].name == "item_06"
        assert items[2].name == "item_07"
        assert items[3].name == "item_08"
        assert items[4].name == "item_09"

    async def test_get_items_with_no_results(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No items in the database.
        WHEN: Items are requested.
        THEN: An empty list is returned.
        """
        query = select(DbTestItem)
        pagination_query = PaginationQuery(page=1, page_size=10)
        items = await _get_items(db_session, query, TestItemSchema, pagination_query)

        assert items == []


@pytest.mark.asyncio
class TestGetPaginatedResponseFunction:
    """
    Tests for get_paginated_response function.
    """

    async def test_get_paginated_response_first_page(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: A paginated response is requested for the first page.
        THEN: The correct paginated response is returned.
        """
        for i in range(15):
            item = DbTestItem(name=f"item_{i:02d}", category="test")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem).order_by(DbTestItem.name)
        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_paginated_response(
            db_session,
            query,
            TestItemSchema,
            pagination_query,
        )

        assert isinstance(response, PaginatedResponse)
        assert len(response.items) == 10
        assert response.total == 15
        assert response.page == 1
        assert response.page_size == 10
        assert response.total_pages == 2
        assert response.has_next is True
        assert response.has_previous is False

    async def test_get_paginated_response_last_page(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: A paginated response is requested for the last page.
        THEN: The correct paginated response is returned.
        """
        for i in range(15):
            item = DbTestItem(name=f"item_{i:02d}", category="test")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem).order_by(DbTestItem.name)
        pagination_query = PaginationQuery(page=2, page_size=10)
        response = await get_paginated_response(
            db_session,
            query,
            TestItemSchema,
            pagination_query,
        )

        assert isinstance(response, PaginatedResponse)
        assert len(response.items) == 5
        assert response.total == 15
        assert response.page == 2
        assert response.page_size == 10
        assert response.has_next is False
        assert response.has_previous is True

    async def test_get_paginated_response_empty_result(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: No items in the database.
        WHEN: A paginated response is requested.
        THEN: An empty paginated response is returned.
        """
        query = select(DbTestItem)
        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_paginated_response(
            db_session,
            query,
            TestItemSchema,
            pagination_query,
        )

        assert isinstance(response, PaginatedResponse)
        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_previous is False

    async def test_get_paginated_response_with_filter(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different categories.
        WHEN: A paginated response is requested with a filter.
        THEN: Only matching items are included in the response.
        """
        for i in range(5):
            item = DbTestItem(name=f"item_{i}", category="alpha")
            db_session.add(item)
        for i in range(3):
            item = DbTestItem(name=f"item_{i + 5}", category="beta")
            db_session.add(item)
        await db_session.flush()

        query = select(DbTestItem).where(DbTestItem.category == "alpha")
        pagination_query = PaginationQuery(page=1, page_size=10)
        response = await get_paginated_response(
            db_session,
            query,
            TestItemSchema,
            pagination_query,
        )

        assert len(response.items) == 5
        assert response.total == 5
        assert all(item.category == "alpha" for item in response.items)

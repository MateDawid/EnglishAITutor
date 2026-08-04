import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils_tests.conftest import DbTestItem
from utils.sorting.services.sorting_service import (
    _preprocess_field,
    get_db_query_with_ordering,
)


class TestPreprocessFieldFunction:
    """
    Tests for _preprocess_field function.
    """

    @pytest.mark.parametrize(
        "field,result",
        [
            ("name", "name"),
            ("-name", "name"),
            ("--name", "name"),
            ("  name  ", "name"),
            ("  -name  ", "name"),
            ("", None),
            ("   ", None),
            ("-", None),
            ("--", None),
        ],
    )
    def test_preprocess_field(self, field: str, result: str | None):
        """
        GIVEN: Various field name formats.
        WHEN: _preprocess_field is called.
        THEN: The expected result is returned.
        """
        assert _preprocess_field(field) == result


@pytest.mark.asyncio
class TestGetDbQueryWithOrderingFunction:
    """
    Tests for get_db_query_with_ordering function.
    """

    async def test_get_db_query_with_ordering_none(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A query and order_by=None.
        WHEN: get_db_query_with_ordering is called.
        THEN: The original query is returned unchanged.
        """
        query = select(DbTestItem)
        result_query = get_db_query_with_ordering(query, None)

        assert result_query == query

    async def test_get_db_query_with_ordering_single_field_ascending(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are sorted by name ascending.
        THEN: Items are returned in correct order.
        """
        item1 = DbTestItem(name="Charlie", category="test", priority=1)
        item2 = DbTestItem(name="Alice", category="test", priority=2)
        item3 = DbTestItem(name="Bob", category="test", priority=3)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, "name")
        result = await db_session.execute(sorted_query)
        items = result.scalars().all()

        assert len(items) == 3
        assert items[0].name == "Alice"
        assert items[1].name == "Bob"
        assert items[2].name == "Charlie"

    async def test_get_db_query_with_ordering_single_field_descending(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are sorted by name descending.
        THEN: Items are returned in reverse order.
        """
        item1 = DbTestItem(name="Charlie", category="test", priority=1)
        item2 = DbTestItem(name="Alice", category="test", priority=2)
        item3 = DbTestItem(name="Bob", category="test", priority=3)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, "-name")
        result = await db_session.execute(sorted_query)
        items = result.scalars().all()

        assert len(items) == 3
        assert items[0].name == "Charlie"
        assert items[1].name == "Bob"
        assert items[2].name == "Alice"

    async def test_get_db_query_with_ordering_multiple_fields(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with same categories but different priorities.
        WHEN: Items are sorted by category ascending and priority descending.
        THEN: Items are returned in correct order.
        """
        item1 = DbTestItem(name="Item1", category="alpha", priority=1)
        item2 = DbTestItem(name="Item2", category="alpha", priority=3)
        item3 = DbTestItem(name="Item3", category="beta", priority=2)
        item4 = DbTestItem(name="Item4", category="alpha", priority=2)
        db_session.add_all([item1, item2, item3, item4])
        await db_session.flush()

        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, "category,-priority")
        result = await db_session.execute(sorted_query)
        items = result.scalars().all()

        assert len(items) == 4
        assert items[0].category == "alpha" and items[0].priority == 3
        assert items[1].category == "alpha" and items[1].priority == 2
        assert items[2].category == "alpha" and items[2].priority == 1
        assert items[3].category == "beta" and items[3].priority == 2

    async def test_get_db_query_with_ordering_with_whitespace(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An order_by string with extra whitespace.
        WHEN: get_db_query_with_ordering is called.
        THEN: Whitespace is handled correctly and items are sorted.
        """
        item1 = DbTestItem(name="Charlie", category="test", priority=1)
        item2 = DbTestItem(name="Alice", category="test", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, " name , -priority ")
        result = await db_session.execute(sorted_query)
        items = result.scalars().all()

        assert len(items) == 2
        assert items[0].name == "Alice"

    async def test_get_db_query_with_ordering_empty_string(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An empty order_by string.
        WHEN: get_db_query_with_ordering is called.
        THEN: The original query is returned unchanged.
        """
        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, "")

        assert sorted_query == query

    async def test_get_db_query_with_ordering_invalid_field_raises(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: An order_by string with an invalid field name.
        WHEN: get_db_query_with_ordering is called.
        THEN: ValueError is raised.
        """
        query = select(DbTestItem)

        with pytest.raises(ValueError, match="Field 'invalid_field' not found"):
            get_db_query_with_ordering(query, "invalid_field")

    async def test_get_db_query_with_ordering_integer_field(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different priorities.
        WHEN: Items are sorted by priority.
        THEN: Items are returned in correct numerical order.
        """
        item1 = DbTestItem(name="Item1", category="test", priority=10)
        item2 = DbTestItem(name="Item2", category="test", priority=2)
        item3 = DbTestItem(name="Item3", category="test", priority=5)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        sorted_query = get_db_query_with_ordering(query, "priority")
        result = await db_session.execute(sorted_query)
        items = result.scalars().all()

        assert len(items) == 3
        assert items[0].priority == 2
        assert items[1].priority == 5
        assert items[2].priority == 10

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils_tests.conftest import DbTestItem
from utils.filtering.services.filtering_service import _is_exact_match, get_db_query_with_filtering


class TestIsExactMatchFunction:
    """
    Tests for _is_exact_match function.
    """

    @pytest.mark.parametrize(
        "filter_value,result",
        [
            ('"exact"', True),
            ('"test value"', True),
            ('""', True),
            ('"', False),
            ("test", False),
            ('test"', False),
            ('"test', False),
            ("", False),
            ('test "value"', False),
        ],
    )
    def test_is_exact_match(self, filter_value: str, result: bool):
        """
        GIVEN: Various filter value formats.
        WHEN: _is_exact_match is called.
        THEN: The expected result is returned.
        """
        assert _is_exact_match(filter_value) == result


@pytest.mark.asyncio
class TestGetDbQueryWithFilteringFunction:
    """
    Tests for get_db_query_with_filtering function.
    """

    async def test_get_db_query_with_filtering_empty_filters(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A query and empty filters.
        WHEN: get_db_query_with_filtering is called.
        THEN: The original query is returned unchanged.
        """
        query = select(DbTestItem)
        result_query = get_db_query_with_filtering(query, {})

        assert result_query == query

    @pytest.mark.parametrize(
        "filter_value",
        ["Alice", "ALICE", "alice", "ice", "ICE", "Ice"],
    )
    async def test_get_db_query_with_filtering_substring_match(self, db_session: AsyncSession, filter_value: str):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are filtered by substring match.
        THEN: Only matching items are returned.
        """
        item1 = DbTestItem(name="Alice Smith", category="test", priority=1)
        item2 = DbTestItem(name="Bob Johnson", category="test", priority=2)
        item3 = DbTestItem(name="Alice Brown", category="test", priority=3)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": filter_value})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2
        assert all("Alice" in item.name for item in items)

    async def test_get_db_query_with_filtering_exact_match(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are filtered by exact match.
        THEN: Only exact matching items are returned.
        """
        item1 = DbTestItem(name="test", category="alpha", priority=1)
        item2 = DbTestItem(name="test value", category="beta", priority=2)
        item3 = DbTestItem(name="test", category="gamma", priority=3)
        item4 = DbTestItem(name="TEST", category="theta", priority=4)
        db_session.add_all([item1, item2, item3, item4])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": '"test"'})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2
        assert all(item.name == "test" for item in items)

    async def test_get_db_query_with_filtering_case_insensitive(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different casing.
        WHEN: Items are filtered with substring match.
        THEN: Case-insensitive matching is performed.
        """
        item1 = DbTestItem(name="UPPERCASE", category="test", priority=1)
        item2 = DbTestItem(name="lowercase", category="test", priority=2)
        item3 = DbTestItem(name="MixedCase", category="test", priority=3)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "case"})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 3

    async def test_get_db_query_with_filtering_multiple_fields(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are filtered by multiple fields.
        THEN: Only items matching all filters are returned.
        """
        item1 = DbTestItem(name="Alice", category="alpha", priority=1)
        item2 = DbTestItem(name="Alice", category="beta", priority=2)
        item3 = DbTestItem(name="Bob", category="alpha", priority=3)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "Alice", "category": "alpha"})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 1
        assert items[0].name == "Alice"
        assert items[0].category == "alpha"

    async def test_get_db_query_with_filtering_with_whitespace(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Filter values with extra whitespace.
        WHEN: get_db_query_with_filtering is called.
        THEN: Whitespace is handled correctly.
        """
        item1 = DbTestItem(name="test", category="alpha", priority=1)
        item2 = DbTestItem(name="other", category="beta", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "  test  "})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 1
        assert items[0].name == "test"

    async def test_get_db_query_with_filtering_empty_value(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A filter with empty value.
        WHEN: get_db_query_with_filtering is called.
        THEN: The filter is ignored.
        """
        item1 = DbTestItem(name="test1", category="alpha", priority=1)
        item2 = DbTestItem(name="test2", category="beta", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": ""})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2

    async def test_get_db_query_with_filtering_none_value(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: A filter with None value.
        WHEN: get_db_query_with_filtering is called.
        THEN: The filter is ignored.
        """
        item1 = DbTestItem(name="test1", category="alpha", priority=1)
        item2 = DbTestItem(name="test2", category="beta", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": None})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2

    async def test_get_db_query_with_filtering_no_matches(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Items that don't match the filter.
        WHEN: get_db_query_with_filtering is called.
        THEN: An empty result is returned.
        """
        item1 = DbTestItem(name="Alice", category="alpha", priority=1)
        item2 = DbTestItem(name="Bob", category="beta", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "Charlie"})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 0

    async def test_get_db_query_with_filtering_partial_match(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Items with partial matching text.
        WHEN: Items are filtered by substring.
        THEN: All items containing the substring are returned.
        """
        item1 = DbTestItem(name="prefix_test", category="alpha", priority=1)
        item2 = DbTestItem(name="test_suffix", category="beta", priority=2)
        item3 = DbTestItem(name="mid_test_value", category="gamma", priority=3)
        item4 = DbTestItem(name="nomatch", category="delta", priority=4)
        db_session.add_all([item1, item2, item3, item4])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "test"})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 3
        assert all("test" in item.name for item in items)

    async def test_get_db_query_with_filtering_exact_match_with_whitespace(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Exact match filter with extra whitespace.
        WHEN: get_db_query_with_filtering is called.
        THEN: Whitespace is stripped from the value.
        """
        item1 = DbTestItem(name="test", category="alpha", priority=1)
        item2 = DbTestItem(name="test value", category="beta", priority=2)
        db_session.add_all([item1, item2])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": '  "test"  '})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 1
        assert items[0].name == "test"

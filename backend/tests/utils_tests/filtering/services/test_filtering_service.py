from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils_tests.conftest import DbTestItem, EnumChoice
from utils.filtering.services.filtering_service import (
    _is_exact_match,
    _filter_by_string_column,
    _filter_by_enum_column,
    filter_by_column,
    get_db_query_with_filtering,
)


class TestIsExactMatchFunction:
    """
    Tests for _is_exact_match function.
    """

    @pytest.mark.parametrize(
        "filter_value,result",
        [
            ('"exact"', True),
            ('"test value"', True),
            ('""', False),
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


class TestFilterByStringColumnFunction:
    """
    Tests for _filter_by_string_column function.
    """

    def test_filter_by_string_column_substring_match(self):
        """
        GIVEN: A query and a string column with substring value.
        WHEN: _filter_by_string_column is called.
        THEN: A query with ILIKE filter is returned.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["name"]

        filtered_query = _filter_by_string_column(query, column, "test")

        assert filtered_query != query
        assert str(filtered_query).lower().count("like") > 0

    def test_filter_by_string_column_exact_match(self):
        """
        GIVEN: A query and a string column with exact match value.
        WHEN: _filter_by_string_column is called.
        THEN: A query with equals filter is returned.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["name"]

        filtered_query = _filter_by_string_column(query, column, '"test"')

        assert filtered_query != query
        assert str(filtered_query).lower().count("like") == 0

    def test_filter_by_string_column_with_whitespace(self):
        """
        GIVEN: A query and a string column with value containing whitespace.
        WHEN: _filter_by_string_column is called.
        THEN: Whitespace is stripped from the value.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["name"]

        filtered_query = _filter_by_string_column(query, column, "  test  ")

        assert filtered_query != query
        assert filtered_query.whereclause.right.effective_value == "%test%"


class TestFilterByEnumColumnFunction:
    """
    Tests for _filter_by_enum_column function.
    """

    def test_filter_by_enum_column(self):
        """
        GIVEN: A query and an enum column with enum value.
        WHEN: _filter_by_enum_column is called.
        THEN: A query with equals filter is returned.
        """

        query = select(DbTestItem)
        column = query.froms[0].columns["enum_field"]

        filtered_query = _filter_by_enum_column(query, column, EnumChoice.VALUE1)

        assert filtered_query != query
        assert isinstance(filtered_query.whereclause.right.effective_value, EnumChoice)
        assert filtered_query.whereclause.right.effective_value == EnumChoice.VALUE1


class TestFilterByColumnFunction:
    """
    Tests for filter_by_column function.
    """

    @patch("utils.filtering.services.filtering_service._filter_by_string_column")
    def test_filter_by_column_with_string_column(self, mock_filter_by_string):
        """
        GIVEN: A query, string column, and string value.
        WHEN: filter_by_column is called.
        THEN: _filter_by_string_column is called with correct parameters.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["name"]
        filter_value = "test"

        mock_filter_by_string.return_value = query

        filter_by_column(query, column, filter_value)

        mock_filter_by_string.assert_called_once_with(query, column, filter_value)

    @patch("utils.filtering.services.filtering_service._filter_by_enum_column")
    def test_filter_by_column_with_enum_column(self, mock_filter_by_enum):
        """
        GIVEN: A query, enum column, and enum value.
        WHEN: filter_by_column is called.
        THEN: _filter_by_enum_column is called with correct parameters.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["enum_field"]
        filter_value = EnumChoice.VALUE1

        mock_filter_by_enum.return_value = query

        filter_by_column(query, column, filter_value)

        mock_filter_by_enum.assert_called_once_with(query, column, filter_value)

    def test_filter_by_column_with_integer_column(self):
        """
        GIVEN: A query, integer column, and integer value.
        WHEN: filter_by_column is called.
        THEN: Unchanged query returned. Integer columns not handled.
        """
        query = select(DbTestItem)
        column = query.froms[0].columns["priority"]
        filter_value = 1

        filtered_query = filter_by_column(query, column, filter_value)
        assert filtered_query == query


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
    async def test_get_db_query_with_filtering_substring_match(
        self,
        db_session: AsyncSession,
        filter_value: str,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are filtered by substring match with various casings.
        THEN: Only matching items are returned (case-insensitive).
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

    async def test_get_db_query_with_filtering_enum_field(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different enum values.
        WHEN: Items are filtered by enum field.
        THEN: Only items matching the enum value are returned.
        """
        item1 = DbTestItem(name="test1", category="alpha", priority=1, enum_field=EnumChoice.VALUE1)
        item2 = DbTestItem(name="test2", category="beta", priority=2, enum_field=EnumChoice.VALUE2)
        item3 = DbTestItem(name="test3", category="gamma", priority=3, enum_field=EnumChoice.VALUE1)
        item4 = DbTestItem(name="test4", category="delta", priority=4, enum_field=None)
        db_session.add_all([item1, item2, item3, item4])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"enum_field": EnumChoice.VALUE1})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2
        assert all(item.enum_field == EnumChoice.VALUE1 for item in items)

    async def test_get_db_query_with_filtering_enum_field_value2(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different enum values.
        WHEN: Items are filtered by enum field with VALUE2.
        THEN: Only items with VALUE2 are returned.
        """
        item1 = DbTestItem(name="test1", category="alpha", priority=1, enum_field=EnumChoice.VALUE1)
        item2 = DbTestItem(name="test2", category="beta", priority=2, enum_field=EnumChoice.VALUE2)
        item3 = DbTestItem(name="test3", category="gamma", priority=3, enum_field=EnumChoice.VALUE2)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"enum_field": EnumChoice.VALUE2})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 2
        assert all(item.enum_field == EnumChoice.VALUE2 for item in items)

    async def test_get_db_query_with_filtering_enum_and_string_fields(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items in the database.
        WHEN: Items are filtered by both enum and string fields.
        THEN: Only items matching both filters are returned.
        """
        item1 = DbTestItem(name="Alice", category="alpha", priority=1, enum_field=EnumChoice.VALUE1)
        item2 = DbTestItem(name="Alice", category="beta", priority=2, enum_field=EnumChoice.VALUE2)
        item3 = DbTestItem(name="Bob", category="gamma", priority=3, enum_field=EnumChoice.VALUE1)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"name": "Alice", "enum_field": EnumChoice.VALUE1})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 1
        assert items[0].name == "Alice"
        assert items[0].enum_field == EnumChoice.VALUE1

    async def test_get_db_query_with_filtering_integer_field(
        self,
        db_session: AsyncSession,
    ):
        """
        GIVEN: Multiple items with different priority values.
        WHEN: Items are filtered by integer field.
        THEN: Query is unchanged as integer filtering is not implemented.
        """
        item1 = DbTestItem(name="test1", category="alpha", priority=1)
        item2 = DbTestItem(name="test2", category="beta", priority=2)
        item3 = DbTestItem(name="test3", category="gamma", priority=1)
        db_session.add_all([item1, item2, item3])
        await db_session.flush()

        query = select(DbTestItem)
        filtered_query = get_db_query_with_filtering(query, {"priority": 1})
        result = await db_session.execute(filtered_query)
        items = result.scalars().all()

        assert len(items) == 3

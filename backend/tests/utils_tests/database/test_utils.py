import pytest
from sqlalchemy import select, Column

from utils.database.utils import get_table_from_select_query, get_column_from_table
from utils_tests.conftest import DbTestItem


class TestGetTableFromSelectQueryFunction:
    """
    Tests for get_table_from_select_query function.
    """

    def test_get_table_from_select_query(self):
        """
        GIVEN: A valid SQLAlchemy Select query.
        WHEN: get_table_from_select_query is called.
        THEN: The correct table is returned.
        """
        query = select(DbTestItem)
        table = get_table_from_select_query(query)

        assert table is not None
        assert hasattr(table, "columns")

    def test_get_table_raises_for_empty_query(self):
        """
        GIVEN: A Select query without a FROM clause.
        WHEN: get_table_from_select_query is called.
        THEN: ValueError is raised.
        """
        query = select()

        with pytest.raises(ValueError, match="Cannot determine table from empty query"):
            get_table_from_select_query(query)


class TestGetColumnFromTableFunction:
    """
    Tests for get_column_from_table function.
    """

    def test_get_column_with_valid_field(self):
        """
        GIVEN: A table and a valid field name.
        WHEN: get_column_from_table is called.
        THEN: The correct column is returned.
        """
        query = select(DbTestItem)
        table = get_table_from_select_query(query)
        column = get_column_from_table(table, "name")

        assert column is not None
        assert isinstance(column, Column)
        assert column.name == "name"

    def test_get_column_with_multiple_valid_fields(self):
        """
        GIVEN: A table and various valid field names.
        WHEN: get_column_from_table is called for each.
        THEN: The correct columns are returned.
        """
        query = select(DbTestItem)
        table = get_table_from_select_query(query)

        name_column = get_column_from_table(table, "name")
        category_column = get_column_from_table(table, "category")
        priority_column = get_column_from_table(table, "priority")

        assert name_column.name == "name"
        assert category_column.name == "category"
        assert priority_column.name == "priority"

    def test_get_column_raises_for_invalid_field(self):
        """
        GIVEN: A table and an invalid field name.
        WHEN: get_column_from_table is called.
        THEN: ValueError is raised.
        """
        query = select(DbTestItem)
        table = get_table_from_select_query(query)

        with pytest.raises(ValueError, match="Field 'invalid_field' not found"):
            get_column_from_table(table, "invalid_field")

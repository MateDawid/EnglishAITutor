import logging

from enum import Enum

from utils.database.utils import get_table_from_select_query, get_column_from_table
from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum, String as SQLString

from utils.types import SelectType

LOGGER = logging.getLogger(__name__)


def filter_by_column(query: SelectType, column: Column, filter_value: str | Enum) -> SelectType:
    """
    Filter database query by given value in specified column.

    Args:
        query (SelectType): Database query.
        column (Column): Column to filter by.
        filter_value (str | Enum): Filter value.

    Returns:
        SelectType: Filtered database query.
    """
    match (column.type, filter_value):
        case (SQLEnum(), Enum()):
            return _filter_by_enum_column(query, column, filter_value)
        case (SQLString(), str()):
            return _filter_by_string_column(query, column, filter_value)
        case _:
            LOGGER.warning(f'Filtering not possible for column type "{repr(column.type)}" and value "{filter_value}"')
            return query


def _filter_by_enum_column(query: SelectType, column: Column, filter_value: Enum) -> SelectType:
    """
    Filter database query by given value in specified Enum column.

    Args:
        query (SelectType): Database query.
        column (Column): Column to filter by.
        filter_value (Enum): Filter value.

    Returns:
        SelectType: Filtered database query.
    """
    return query.where(column == filter_value)


def _filter_by_string_column(query: SelectType, column: Column, filter_value: str) -> SelectType:
    """
    Filter database query by given value in specified String column.

    Args:
        query (SelectType): Database query.
        column (Column): Column to filter by.
        filter_value (str): Filter value.

    Returns:
        SelectType: Filtered database query.
    """
    filter_value = filter_value.strip()
    if _is_exact_match(filter_value):
        return query.where(column == filter_value.strip('"'))
    else:
        return query.where(column.ilike(f"%{filter_value}%"))


def _is_exact_match(filter_value: str) -> bool:
    """
    Checks if string filter is for exact or partial match.

    Args:
        filter_value (str): The string filter value.

    Returns:
        bool: True if the filter is for an exact match, False otherwise.
    """
    return len(filter_value) > 2 and filter_value.startswith('"') and filter_value.endswith('"')


def get_db_query_with_filtering(query: SelectType, filters: dict[str, str | Enum]) -> SelectType:
    """
    Filter database query by given filter values.

    Args:
        query (SelectType): Database query.
        filters (dict[str, str | Enum]): Filter values.

    Returns:
        SelectType: Filtered database query.
    """
    table = get_table_from_select_query(query)
    for field, filter_value in filters.items():
        if not filter_value:
            continue
        column = get_column_from_table(table, field)
        query = filter_by_column(query, column, filter_value)
    return query

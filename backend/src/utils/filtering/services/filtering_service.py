from typing import Any

from utils.database.utils import get_table_from_select_query, get_column_from_table

from utils.types import SelectType


def _is_exact_match(filter_value: str) -> bool:
    """
    Check if the word is an exact match (enclosed in double quotes).

    Args:
        filter_value (str): The word to check.
    """
    return filter_value.startswith('"') and filter_value.endswith('"')


def get_db_query_with_filtering(query: SelectType, filters: dict[str, Any]) -> SelectType:
    """
    Filter database query based on filters parameter.

    Args:
        query (SelectType): SQLAlchemy Select query to filter
        filters (dict[str, Any]): The filters query parameters.

    Returns:
        SelectType: Filtered SQLAlchemy Select query
    """
    table = get_table_from_select_query(query)
    for field, filter_value in filters.items():
        if not filter_value:
            continue
        column = get_column_from_table(table, field)
        filter_value = filter_value.strip()
        if _is_exact_match(filter_value):
            query = query.where(column == filter_value.strip('"'))
        else:
            query = query.where(column.ilike(f"%{filter_value}%"))
    return query

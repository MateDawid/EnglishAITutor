from sqlalchemy import desc

from utils.database.utils import get_table_from_select_query, get_column_from_table
from utils.types import SelectType


def _preprocess_field(field: str) -> str | None:
    """
    Preprocess single field extracted from order_by query parameter.

    Args:
        field (str): Field name to preprocess.

    Returns:
        str | None: Preprocessed field name or None if empty.
    """
    field = field.strip().lstrip("-")
    if not field:
        return None
    return field


def get_db_query_with_ordering(query: SelectType, order_by: str | None) -> SelectType:
    """
    Sort database query based on order_by parameter.

    Args:
        query (SelectType): SQLAlchemy Select query to sort
        order_by (str | None): Comma-separated fields, prefix '-' for descending

    Returns:
        SelectType: Sorted SQLAlchemy Select query
    """
    if not order_by:
        return query
    table = get_table_from_select_query(query)
    for field in order_by.split(","):
        field = field.strip()
        if not field:
            continue
        is_descending = field.startswith("-")
        field = _preprocess_field(field)
        if field is None:
            continue
        column = get_column_from_table(table, field)
        query = query.order_by(desc(column) if is_descending else column)
    return query

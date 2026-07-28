from sqlalchemy import desc, FromClause
from utils.types import SelectType


def _get_table(query: SelectType) -> FromClause:
    """
    Get the table from the SQLAlchemy Select query.

    Args:
        query (SelectType): SQLAlchemy Select query.

    Returns:
        FromClause: Database table.

    Raises:
        ValueError: Raised if not from clause in query.
    """
    try:
        return query.froms[0]
    except IndexError:
        raise ValueError("Cannot determine table from empty query")


def _preprocess_field(field: str) -> str | None:
    """
    Preprocess single field extracted from order_by query parameter.

    Args:
        field (str): Field name to preprocess.

    Returns:
        str | None: Preprocessed field name or None if empty.
    """
    field = field.strip()
    if not field:
        return None
    field = field.lstrip("-")
    return field


def _get_column(table: FromClause, field: str):
    """
    Get column with specified name from table.

    Args:
        table (FromClause): Database table.
        field (str): Field name to get column for.

    Returns:
        Column: SQLAlchemy column object.

    Raises:
        ValueError: Raised if field not found in table.
    """
    if hasattr(table, "columns") and hasattr(table.columns, field):
        return getattr(table.columns, field)
    else:
        raise ValueError(f"Field '{field}' not found")


def get_db_query_with_ordering(query: SelectType, order_by: str | None) -> SelectType:
    """
    Sort database query based on order_by parameter.

    Args:
        query (SelectType): SQLAlchemy Select query to sort
        order_by (str | None): Comma-separated fields, prefix '-' for descending

    Returns:
        SelectType: Sorted SQLAlchemy Select query
    """
    if order_by is None:
        return query
    table = _get_table(query)
    for field in order_by.split(","):
        field = field.strip()
        if not field:
            continue
        is_descending = field.startswith("-")
        field = _preprocess_field(field)
        if field is None:
            continue
        column = _get_column(table, field)
        query = query.order_by(desc(column) if is_descending else column)
    return query

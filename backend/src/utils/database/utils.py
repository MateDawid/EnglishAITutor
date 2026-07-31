from sqlalchemy import FromClause, Column
from utils.types import SelectType


def get_table_from_select_query(query: SelectType) -> FromClause:
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


def get_column_from_table(table: FromClause, field: str) -> Column:
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

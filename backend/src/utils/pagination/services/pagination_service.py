from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Select

from utils.pagination.schemas import PaginatedResponse, PaginationQuery
from utils.types import DbModelType, SchemaType


async def _get_total_count(db: AsyncSession, query: Select[tuple[DbModelType]]) -> int:
    """
    Get total count from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        query (Select[tuple[DbModelType]]): The SQLAlchemy query to execute.

    Returns:
        int: The total count of items matching the query.
    """
    total_query = select(func.count()).select_from(query.subquery())
    return await db.scalar(total_query) or 0


async def _get_items(
    db: AsyncSession,
    query: Select[tuple[DbModelType]],
    schema_type: type[SchemaType],
    pagination_query: PaginationQuery,
) -> list[SchemaType]:
    """
    Get paginated items from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        query (Select[tuple[DbModelType]]): The SQLAlchemy query to execute.
        schema_type (type[SchemaType]): The Pydantic schema type for the results.
        pagination_query (PaginationQuery): The pagination query parameters.

    Returns:
        list[SchemaType]: The list of items matching the query.
    """
    result = await db.execute(query.offset(pagination_query.offset).limit(pagination_query.page_size))
    return [schema_type.model_validate(item, from_attributes=True) for item in result.scalars().all()]


async def get_paginated_response(
    db: AsyncSession,
    query: Select[tuple[DbModelType]],
    schema_type: type[SchemaType],
    pagination_query: PaginationQuery,
) -> PaginatedResponse[SchemaType]:
    """
    Get a paginated result from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        query (Select[tuple[DbModelType]]): The SQLAlchemy query to execute.
        schema_type (type[SchemaType]): The Pydantic schema type for the results.
        pagination_query (PaginationQuery): The pagination query parameters.

    Returns:
        PaginatedResponse[SchemaType]: The paginated result.
    """

    total = await _get_total_count(db, query)
    items = await _get_items(db, query, schema_type, pagination_query)

    return PaginatedResponse(
        items=items,
        total=total,
        page=pagination_query.page,
        page_size=pagination_query.page_size,
    )

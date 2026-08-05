from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.filtering.services.filtering_service import get_db_query_with_filtering
from utils.sorting import get_db_query_with_ordering
from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from utils.pagination import get_paginated_response, PaginationQuery, PaginatedResponse


async def get_flashcards_from_db(
    db: AsyncSession,
    pagination_query: PaginationQuery,
    order_by: str | None,
    filters: dict[str, Any],
) -> PaginatedResponse[FlashcardSchema]:
    """
    Get the list of flashcards from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (str | None): The order by query parameters.
        filters (dict[str, Any]): The filters query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    query = select(DbFlashcard)
    query = get_db_query_with_filtering(query=query, filters=filters)
    query = get_db_query_with_ordering(query=query, order_by=order_by)
    response = await get_paginated_response(
        db=db, query=query, schema_type=FlashcardSchema, pagination_query=pagination_query
    )
    return response

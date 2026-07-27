from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.sorting import OrderByField, get_db_query_with_ordering
from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from utils.pagination import get_paginated_response, PaginationQuery, PaginatedResponse


async def get_flashcards_from_db(
    db: AsyncSession, pagination_query: PaginationQuery, order_by: OrderByField | None
) -> PaginatedResponse[FlashcardSchema]:
    """
    Get the list of flashcards from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        pagination_query (PaginationQuery): The pagination query parameters.
        order_by (OrderByField | None): The order by query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """
    query = get_db_query_with_ordering(query=select(DbFlashcard), order_by=order_by)
    response = await get_paginated_response(
        db=db, query=query, schema_type=FlashcardSchema, pagination_query=pagination_query
    )
    return response

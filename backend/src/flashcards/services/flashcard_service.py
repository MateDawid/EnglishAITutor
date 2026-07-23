from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from flashcards.models import DbFlashcard
from flashcards.schemas import FlashcardSchema
from pagination import get_paginated_response, PaginationQuery, PaginatedResponse


async def get_flashcards_from_db(
    db: AsyncSession, pagination_query: PaginationQuery
) -> PaginatedResponse[FlashcardSchema]:
    """
    Get the list of flashcards from the database.

    Args:
        db (AsyncSession): The database session to use for the query.
        pagination_query (PaginationQuery): The pagination query parameters.

    Returns:
        PaginatedResponse[FlashcardSchema]: The paginated result.
    """

    response = await get_paginated_response(
        db=db, query=select(DbFlashcard), schema_type=FlashcardSchema, pagination_query=pagination_query
    )
    return response

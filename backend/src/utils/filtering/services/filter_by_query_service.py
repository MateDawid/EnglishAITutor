from fastapi import Query
from fastapi.params import Query as QueryClass
from fastapi.openapi.models import Example


def FilterByStringQuery() -> QueryClass:
    """
    Function for creating a FastAPI query parameter for filtering by specified fields.

    Returns:
        Query: A FastAPI Query parameter for filtering by the specified fields.
    """
    return Query(
        openapi_examples={
            "example": Example(value="example", summary="Filter by substring 'example'"),
            '"example"': Example(value='"example"', summary="Filter by exact value 'example'"),
        }
    )

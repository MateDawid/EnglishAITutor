from typing import TypeVar

from sqlalchemy import Select

from utils.types import DbModelType

# 1. single field from specified choices in ascending order, like order_by=field1
# 2. single field from specified choices in descending order (with leading '-'), like order_by=-field1
# 3. multiple, comma-separated fields from specified choices, like order_by=field1,-field2,field3

OrderByField = TypeVar("OrderByField", bound=str)


def get_db_query_with_ordering(
    query: Select[tuple[DbModelType]], order_by: OrderByField | None
) -> Select[tuple[DbModelType]]:
    if order_by is None:
        return query
    if order_by.startswith("-"):
        # TODO - order by desc
        order_by = order_by.lstrip("-")
    if "," in order_by:
        # TODO - order by many fields
        order_by = order_by.split(",")[0]
    return query.order_by(order_by)

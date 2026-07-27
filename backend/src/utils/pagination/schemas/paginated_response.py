from typing import Generic

from pydantic import BaseModel, computed_field

from utils.types import SchemaType


class PaginatedResponse(BaseModel, Generic[SchemaType]):
    """
    Standard paginated response structure
    """

    model_config = {"arbitrary_types_allowed": True}

    items: list[SchemaType]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        """
        Calculates the total number of pages.

        Returns:
            int: The total number of pages based on the total items and page size.
        """
        return (self.total + self.page_size - 1) // self.page_size if self.total > 0 else 0

    @computed_field
    @property
    def has_next(self) -> bool:
        """
        Checks if there is a next page.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        return self.page < self.total_pages

    @computed_field
    @property
    def has_previous(self) -> bool:
        """
        Checks if there is a previous page.

        Returns:
            bool: True if there is a previous page, False otherwise.
        """
        return self.page > 1

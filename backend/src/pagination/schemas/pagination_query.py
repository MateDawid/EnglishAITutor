from pydantic import BaseModel, Field, computed_field

MAX_RESULTS_PER_PAGE = 50
DEFAULT_PAGE_SIZE = 10


class PaginationQuery(BaseModel):
    """
    Model passed in the request to validate pagination input.
    """

    page: int = Field(default=1, ge=1, description="Requested page number")
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_RESULTS_PER_PAGE,
        description="Requested number of items per page",
    )

    @computed_field
    @property
    def offset(self) -> int:
        """
        Calculates the offset for pagination.

        Returns:
            int: The offset value based on the current page and page size.
        """
        return (self.page - 1) * self.page_size

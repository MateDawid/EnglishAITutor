import pytest

from utils.pagination.schemas import PaginationQuery
from utils.pagination.schemas.pagination_query import MAX_RESULTS_PER_PAGE, DEFAULT_PAGE_SIZE


class TestPaginationQuerySchema:
    """
    Tests for PaginationQuery schema.
    """

    def test_pagination_query_defaults(self):
        """
        GIVEN: No parameters provided.
        WHEN: PaginationQuery is instantiated.
        THEN: Default values are used (page=1, page_size=10).
        """
        query = PaginationQuery()

        assert query.page == 1
        assert query.page_size == DEFAULT_PAGE_SIZE
        assert query.offset == 0

    def test_pagination_query_with_custom_values(self):
        """
        GIVEN: Custom page and page_size values.
        WHEN: PaginationQuery is instantiated.
        THEN: The provided values are used.
        """
        query = PaginationQuery(page=3, page_size=20)

        assert query.page == 3
        assert query.page_size == 20
        assert query.offset == 40

    @pytest.mark.parametrize(
        "page,page_size,expected_offset",
        [
            (1, 10, 0),
            (2, 10, 10),
            (1, 50, 0),
            (3, 25, 50),
            (10, 5, 45),
        ],
    )
    def test_pagination_query_offset_calculation(
        self,
        page: int,
        page_size: int,
        expected_offset: int,
    ):
        """
        GIVEN: Different page and page_size combinations.
        WHEN: The offset is calculated.
        THEN: The offset matches the expected value.
        """
        query = PaginationQuery(page=page, page_size=page_size)

        assert query.offset == expected_offset

    def test_pagination_query_raises_for_page_less_than_one(self):
        """
        GIVEN: A page number less than 1.
        WHEN: PaginationQuery is instantiated.
        THEN: Validation error is raised.
        """
        with pytest.raises(ValueError):
            PaginationQuery(page=0)

    def test_pagination_query_raises_for_negative_page(self):
        """
        GIVEN: A negative page number.
        WHEN: PaginationQuery is instantiated.
        THEN: Validation error is raised.
        """
        with pytest.raises(ValueError):
            PaginationQuery(page=-1)

    def test_pagination_query_raises_for_page_size_less_than_one(self):
        """
        GIVEN: A page_size less than 1.
        WHEN: PaginationQuery is instantiated.
        THEN: Validation error is raised.
        """
        with pytest.raises(ValueError):
            PaginationQuery(page_size=0)

    def test_pagination_query_raises_for_page_size_greater_than_max(self):
        """
        GIVEN: A page_size greater than the maximum allowed.
        WHEN: PaginationQuery is instantiated.
        THEN: Validation error is raised.
        """
        with pytest.raises(ValueError):
            PaginationQuery(page_size=MAX_RESULTS_PER_PAGE + 1)

    def test_pagination_query_allows_max_page_size(self):
        """
        GIVEN: A page_size equal to the maximum allowed.
        WHEN: PaginationQuery is instantiated.
        THEN: The value is accepted.
        """
        query = PaginationQuery(page_size=MAX_RESULTS_PER_PAGE)

        assert query.page_size == MAX_RESULTS_PER_PAGE

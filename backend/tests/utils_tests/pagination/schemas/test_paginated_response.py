import pytest
from pydantic import BaseModel

from utils.pagination.schemas import PaginatedResponse


class TestItemSchema(BaseModel):
    """
    Test schema for pagination tests.
    """

    id: int
    name: str


class TestPaginatedResponseSchema:
    """
    Tests for PaginatedResponse schema.
    """

    def test_paginated_response_creation(self):
        """
        GIVEN: Items and pagination metadata.
        WHEN: PaginatedResponse is instantiated.
        THEN: All fields are set correctly.
        """
        items = [
            TestItemSchema(id=1, name="Item 1"),
            TestItemSchema(id=2, name="Item 2"),
        ]

        response = PaginatedResponse[TestItemSchema](
            items=items,
            total=10,
            page=1,
            page_size=2,
        )

        assert response.items == items
        assert response.total == 10
        assert response.page == 1
        assert response.page_size == 2

    @pytest.mark.parametrize(
        "total,page_size,expected_total_pages",
        [
            (0, 10, 0),
            (1, 10, 1),
            (10, 10, 1),
            (11, 10, 2),
            (20, 10, 2),
            (21, 10, 3),
            (100, 25, 4),
            (99, 25, 4),
        ],
    )
    def test_paginated_response_total_pages_calculation(
        self,
        total: int,
        page_size: int,
        expected_total_pages: int,
    ):
        """
        GIVEN: Different total and page_size combinations.
        WHEN: total_pages is calculated.
        THEN: It matches the expected value.
        """
        response = PaginatedResponse[TestItemSchema](
            items=[],
            total=total,
            page=1,
            page_size=page_size,
        )

        assert response.total_pages == expected_total_pages

    @pytest.mark.parametrize(
        "page,total_pages,expected_has_next",
        [
            (1, 3, True),
            (2, 3, True),
            (3, 3, False),
            (1, 1, False),
        ],
    )
    def test_paginated_response_has_next(
        self,
        page: int,
        total_pages: int,
        expected_has_next: bool,
    ):
        """
        GIVEN: Different page and total_pages combinations.
        WHEN: has_next is accessed.
        THEN: It matches the expected value.
        """
        total = total_pages * 10
        response = PaginatedResponse[TestItemSchema](
            items=[],
            total=total,
            page=page,
            page_size=10,
        )

        assert response.has_next == expected_has_next

    @pytest.mark.parametrize(
        "page,expected_has_previous",
        [
            (1, False),
            (2, True),
            (3, True),
            (10, True),
        ],
    )
    def test_paginated_response_has_previous(
        self,
        page: int,
        expected_has_previous: bool,
    ):
        """
        GIVEN: Different page numbers.
        WHEN: has_previous is accessed.
        THEN: It matches the expected value.
        """
        response = PaginatedResponse[TestItemSchema](
            items=[],
            total=100,
            page=page,
            page_size=10,
        )

        assert response.has_previous == expected_has_previous

    def test_paginated_response_empty_result(self):
        """
        GIVEN: A response with no items and total of 0.
        WHEN: The response is created.
        THEN: Pagination metadata is handled correctly.
        """
        response = PaginatedResponse[TestItemSchema](
            items=[],
            total=0,
            page=1,
            page_size=10,
        )

        assert response.items == []
        assert response.total == 0
        assert response.total_pages == 0
        assert response.has_next is False
        assert response.has_previous is False

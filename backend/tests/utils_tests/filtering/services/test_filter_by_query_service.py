from utils.filtering.services.filter_by_query_service import FilterByStringQuery
from fastapi.params import Query as QueryClass


class TestFilterByStringQueryFunction:
    """
    Tests for FilterByStringQuery function.
    """

    def test_filter_by_string_query_creates_valid_query_parameter(self):
        """
        GIVEN: FilterByStringQuery is called.
        WHEN: A Query parameter is created.
        THEN: A valid Query parameter is returned.
        """
        query_param = FilterByStringQuery()

        assert query_param is not None
        assert isinstance(query_param, QueryClass)

    def test_filter_by_string_query_has_examples(self):
        """
        GIVEN: FilterByStringQuery is called.
        WHEN: OpenAPI examples are accessed.
        THEN: Examples for substring and exact match are present.
        """
        query_param = FilterByStringQuery()

        assert query_param.openapi_examples is not None
        assert len(query_param.openapi_examples) == 2
        assert "example" in query_param.openapi_examples
        assert '"example"' in query_param.openapi_examples

    def test_filter_by_string_query_example_values(self):
        """
        GIVEN: FilterByStringQuery is called.
        WHEN: Example values are inspected.
        THEN: Correct values and summaries are set.
        """
        query_param = FilterByStringQuery()

        substring_example = query_param.openapi_examples["example"]
        exact_example = query_param.openapi_examples['"example"']

        assert substring_example["value"] == "example"
        assert exact_example["value"] == '"example"'
        assert "substring" in substring_example["summary"].lower()
        assert "exact" in exact_example["summary"].lower()

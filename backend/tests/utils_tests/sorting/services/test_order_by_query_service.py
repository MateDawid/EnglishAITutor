from utils.sorting.services.order_by_query_service import _prepare_order_by_examples, OrderByQuery
from fastapi.params import Query as QueryClass


class TestPrepareOrderByExamplesFunction:
    """
    Tests for _prepare_order_by_examples function.
    """

    def test_prepare_order_by_examples_with_single_choice(self):
        """
        GIVEN: A single field choice.
        WHEN: Examples are prepared.
        THEN: Two examples (ascending and descending) are returned.
        """
        choice_1 = "name"
        choices = [choice_1]
        examples = _prepare_order_by_examples(choices)

        assert len(examples) == 2
        assert choice_1 in examples
        assert f"-{choice_1}" in examples
        assert examples[choice_1]["value"] == choice_1
        assert examples[f"-{choice_1}"]["value"] == f"-{choice_1}"
        assert examples[choice_1]["summary"] == f'Order by "{choice_1}" field ascending'
        assert examples[f"-{choice_1}"]["summary"] == f'Order by "{choice_1}" field descending'

    def test_prepare_order_by_examples_with_multiple_choices(self):
        """
        GIVEN: Multiple field choices.
        WHEN: Examples are prepared.
        THEN: Four examples are returned (single ascending, single descending, combined, and mixed).
        """
        choice_1 = "name"
        choice_2 = "created_at"
        choices = [choice_1, choice_2]
        examples = _prepare_order_by_examples(choices)

        assert len(examples) == 4
        assert choice_1 in examples
        assert f"-{choice_1}" in examples
        assert f"{choice_1},{choice_2}" in examples
        assert f"-{choice_1},{choice_2}" in examples
        assert examples[choice_1]["value"] == choice_1
        assert examples[f"-{choice_1}"]["value"] == f"-{choice_1}"
        assert examples[choice_1]["summary"] == f'Order by "{choice_1}" field ascending'
        assert examples[f"-{choice_1}"]["summary"] == f'Order by "{choice_1}" field descending'
        assert examples[f"{choice_1},{choice_2}"]["value"] == f"{choice_1},{choice_2}"
        assert examples[f"-{choice_1},{choice_2}"]["value"] == f"-{choice_1},{choice_2}"
        assert examples[f"{choice_1},{choice_2}"]["summary"] == f'Order by fields "{choice_1}" and "{choice_2}"'
        assert (
            examples[f"-{choice_1},{choice_2}"]["summary"]
            == f'Order by fields "{choice_1}" descending and "{choice_2}" ascending'
        )

    def test_prepare_order_by_examples_with_three_choices(self):
        """
        GIVEN: Three field choices.
        WHEN: Examples are prepared.
        THEN: Four examples are returned using the first two choices.
        """
        choice_1 = "name"
        choice_2 = "age"
        choice_3 = "status"
        choices = [choice_1, choice_2, choice_3]
        examples = _prepare_order_by_examples(choices)

        assert len(examples) == 4
        assert choice_1 in examples
        assert f"-{choice_1}" in examples
        assert f"{choice_1},{choice_2}" in examples
        assert f"-{choice_1},{choice_2}" in examples
        for key in examples:
            assert choice_3 not in key


class TestOrderByQueryFunction:
    """
    Tests for OrderByQuery function.
    """

    def test_order_by_query_creates_valid_query_parameter(self):
        """
        GIVEN: Field choices for ordering.
        WHEN: OrderByQuery is called.
        THEN: A valid Query parameter is returned.
        """
        choices = ["name", "created_at"]
        query_param = OrderByQuery(choices)

        assert query_param is not None
        assert isinstance(query_param, QueryClass)

    def test_order_by_query_pattern_validation(self):
        """
        GIVEN: Field choices for ordering.
        WHEN: OrderByQuery is called.
        THEN: The pattern correctly validates field combinations.
        """
        choices = ["name", "age"]
        query_param = OrderByQuery(choices)

        assert getattr(query_param.metadata[0], "pattern") == r"^-?(name|age)(,-?(name|age))*$"

    def test_order_by_query_with_single_choice(self):
        """
        GIVEN: A single field choice.
        WHEN: OrderByQuery is called.
        THEN: Pattern and examples are created correctly.
        """
        choices = ["status"]
        query_param = OrderByQuery(choices)

        assert getattr(query_param.metadata[0], "pattern") == r"^-?(status)(,-?(status))*$"
        assert query_param.openapi_examples is not None
        assert len(query_param.openapi_examples) == 2

    def test_order_by_query_with_multiple_choices(self):
        """
        GIVEN: Multiple field choices.
        WHEN: OrderByQuery is called.
        THEN: Pattern and examples include all possibilities.
        """
        choices = ["name", "created_at", "updated_at"]
        query_param = OrderByQuery(choices)

        assert (
            getattr(query_param.metadata[0], "pattern")
            == r"^-?(name|created_at|updated_at)(,-?(name|created_at|updated_at))*$"
        )
        assert len(query_param.openapi_examples) == 4

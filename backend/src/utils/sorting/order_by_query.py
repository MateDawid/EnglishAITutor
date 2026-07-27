from typing import Sequence

from fastapi import Query
from fastapi.params import Query as QueryClass
from fastapi.openapi.models import Example


def _prepare_order_by_examples(choices: Sequence[str]) -> dict[str, Example]:
    """
    Function for creating order_by query parameter examples.

    Args:
        choices: (Sequence[str]): A sequence of field names that can be used for ordering.

    Returns:
        dict[str, Example]: A dictionary of example values for the order_by query parameter.
    """
    examples = {
        f"{choices[0]}": Example(value=choices[0], summary=f'Order by "{choices[0]}" field ascending'),
        f"-{choices[0]}": Example(value=f"-{choices[0]}", summary=f'Order by "{choices[0]}" field descending'),
    }
    if len(choices) > 1:
        examples[f"{choices[0]},{choices[1]}"] = Example(
            value=f"{choices[0]},{choices[1]}", summary=f'Order by fields "{choices[0]}" and "{choices[1]}"'
        )
        examples[f"-{choices[0]},{choices[1]}"] = Example(
            value=f"-{choices[0]},{choices[1]}",
            summary=f'Order by fields "{choices[0]}" descending and "{choices[1]}" ascending',
        )
    return examples


def OrderByQuery(choices: Sequence[str]) -> QueryClass:
    """
    Function for creating a FastAPI query parameter for ordering by specified fields.

    Args:
        choices (Sequence[str]): A sequence of field names that can be used for ordering.

    Returns:
        Query: A FastAPI Query parameter for ordering by the specified fields.
    """
    pattern = r"^-?(" + "|".join(choices) + r")(,-?(" + "|".join(choices) + r"))*$"
    return Query(
        pattern=pattern,
        openapi_examples=_prepare_order_by_examples(choices),
    )

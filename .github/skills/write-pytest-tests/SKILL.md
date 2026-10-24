---
name: write-pytest-tests
description: "Use when asked to write, generate, or create Python tests with pytest, or to update existing pytest tests."
---

# Writing Pytest Tests

Write maintainable Python tests that follow the repository's existing pytest conventions.

## When to Use

- Creating or updating Python tests.
- Refactoring pytest tests or reviewing them for convention compliance.
- Choosing pytest fixtures, parametrization, or async test patterns.

## Conventions

1. **File naming** — Name a test file `test_{tested_file}.py`, where `{tested_file}` is the source module name without `.py`. For example, tests for `flashcard_service.py` belong in `test_flashcard_service.py`. Place tests in the corresponding feature or test directory, following nearby repository structure.
2. **Group related tests in classes** — Use a class for each tested function or cohesive behavior, named `Test{FunctionName}Function` (for example, `TestGetFlashcardsFromDbFunction`). For service or feature behavior, use a descriptive class name. Keep each test focused on one behavior.
3. **GIVEN/WHEN/THEN docstrings** — Every test must have a concise docstring with `GIVEN:`, `WHEN:`, and `THEN:` statements. Describe setup, action, and observable outcome.
4. **Descriptive test names** — Name tests `test_{behavior}_{condition}` and state the expected result, such as `test_hash_password_returns_hashed_value`.
5. **Reuse and extend fixtures and factories** — Use existing fixtures from `conftest.py` and project factories for shared setup, such as database sessions, authenticated users, and model instances. Prefer extending a factory or creating a reusable fixture over building mocks or duplicating setup. Use mocks only when isolation is needed for an external dependency or behavior that cannot reasonably be exercised with a fixture or factory.
6. **Cover input categories** — For each behavior, cover representative normal valid inputs, meaningful edge cases (such as empty collections, boundary values, or optional values), and invalid inputs where the contract defines validation or error behavior. Assert the documented result or error for each category; do not invent behavior for unsupported inputs.
7. **Parametrize cases** — Use `@pytest.mark.parametrize` when the same behavior should be checked against multiple inputs or expected outcomes. Include normal, edge, and invalid cases where they share behavior, with descriptive parameter names; avoid duplicating nearly identical test bodies.
8. **Use pytest tools** — Prefer pytest fixtures and utilities such as `monkeypatch`, `pytest.raises`, and `pytest.mark.parametrize` over custom test frameworks or manual state management. Use project factories to create realistic test data; reserve mocks for dependencies that should not be invoked in the test.
9. **Async tests** — For async tests, follow the repository's pytest-asyncio pattern, including `@pytest.mark.asyncio` where required. Type-annotate fixture and parameter arguments when repository patterns support it.
10. **Testable, decoupled design** — Prefer small, single-responsibility functions, classes, and methods with explicit inputs and outputs. Separate business rules from I/O and framework concerns; inject or pass dependencies rather than relying on hidden global state. Test units through their public behavior, and use fixtures or focused fakes at clear boundaries instead of tests that depend on unrelated implementation details.
11. **Assert outcomes** — Assert externally observable behavior and relevant state changes. Avoid assertions on implementation details unless they are part of the contract.

## Example

```python
import pytest


class TestDivideFunction:
    """Tests for divide."""

    @pytest.mark.parametrize(
        "numerator,denominator,expected",
        [
            (6, 3, 2),
            (5, 2, 2.5),
        ],
    )
    def test_divide_returns_quotient(self, numerator, denominator, expected):
        """
        GIVEN: A numerator and a non-zero denominator.
        WHEN: The numbers are divided.
        THEN: The quotient is returned.
        """
        result = divide(numerator, denominator)

        assert result == expected
```
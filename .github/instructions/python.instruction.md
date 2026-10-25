---
applyTo: ["**/*.py"]
description: 'Create or update Python code.'
---

# Writing code

Follow every rule below for  creating or updating Python code. 

## When to Use
- Creating or updating Python code.
- Reviewing or fixing existing code for convention compliance.

## Golden Rules (non-negotiable)

1. **Docstrings** - Use Google style docstring for every function, class and class method. Follow the example below.
2. **Single responsibility** — each function, class and class method should have a single responsibility.
3. **Separate concerns** — separate business logic from data access, validation, and presentation.
4. **Type hints** — use type hints for all function arguments and return types.
5. **Simplicity** — keep code simple and readable, avoid unnecessary complexity.
6. **Separate files for each class** — each class should be in its own file, named after the class.
7. **Testability and low coupling** — Keep functions, classes, and methods small and single-responsibility so they are easy to test independently. Separate business logic from I/O and framework-specific code. Pass dependencies explicitly or inject them rather than relying on global state, and depend on stable interfaces or protocols instead of concrete implementations where useful. Prefer pure functions for logic that does not need side effects.
8. **Typed structured data** — For fixed, structured values such as complex function arguments or return values, prefer a dataclass with explicitly typed fields over an untyped or loosely typed dictionary. Use dictionaries for genuinely dynamic key-value data, and use existing validation/schema types (such as Pydantic models) at API or input boundaries when runtime validation is needed.
9. **Declaration order** — Declare functions and class methods in invocation order: a caller must appear before the functions or methods it invokes in the same file.

## Docstring example
```python
def divide(numerator: int, denominator: int) -> float | int:
    """
    Divides the first number by the second number.

    Args:
        numerator (int): The numerator.
        denominator (int): The denominator.

    Returns:
        int: Result of the division.
        
    Raises:
        ValueError: If the second number is zero.
    """
    return numerator / denominator
```

Rules:
- Summary line first.
- Arguments section with type hints.
- Returns section with type hints.
- Raises section for exceptions.

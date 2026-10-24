---
applyTo: ["**/*.ts", "**/*.tsx"]
description: 'Create or update TypeScript code.'
---

# Writing code

Follow every rule below when creating or updating TypeScript code.

## When to Use
- Creating or updating TypeScript code.
- Reviewing or fixing existing code for convention compliance.

## Golden Rules (non-negotiable)

1. **Documentation** — Use JSDoc comments for every function, class, and class method. Follow the example below.
2. **Single responsibility** — each function, class and class method should have a single responsibility.
3. **Separate concerns** — separate business logic from data access, validation, and presentation.
4. **Type annotations** — declare types for all function arguments and return values.
5. **Simplicity** — keep code simple and readable, avoid unnecessary complexity.
6. **Separate files for each class** — each class should be in its own file, named after the class.

## Documentation example
```typescript
/**
 * Divides the first number by the second number.
 *
 * @param {number} numerator - The numerator.
 * @param {number} denominator - The denominator.
 * @returns {number} The quotient.
 * @throws {RangeError} If the denominator is zero.
 */
function divide(numerator: number, denominator: number): number {
    if (denominator === 0) {
        throw new RangeError("The denominator must not be zero.");
    }

    return numerator / denominator;
}
```

Rules:
- Summary line first.
- Use `@param` tags to describe parameters with types.
- Use `@returns` to describe the return value with type.
- Use `@throws` to document exceptions when applicable.

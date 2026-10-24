---
name: write-frontend-tests
description: "Use when asked to write, generate, create, or improve frontend unit tests in the frontend directory using Vitest, React Testing Library, and TypeScript."
---

# Writing Frontend Tests

Write reliable, readable TypeScript tests that verify frontend behavior and follow the existing Vitest setup.

## When to Use

- Creating or generating unit tests in `frontend/`.
- Improving or refactoring existing frontend tests.
- Testing React components, hooks, services, or utility functions.

## Conventions

1. **File naming and placement** — Co-locate tests with the code they cover and name them `<tested-file>.test.ts` or `<tested-file>.test.tsx`, matching the project's existing pattern. Use `.tsx` when the test contains JSX.
2. **Group related tests** — Use `describe` blocks named for the component, service, hook, or behavior under test. Keep each `it`/`test` case focused on one observable behavior.
3. **Given/when/then clarity** — Make each test's setup, action, and expected outcome clear. Prefer descriptive test names and straightforward arrange-act-assert structure; add concise `// GIVEN:`, `// WHEN:`, and `// THEN:` comments only when the phases are not self-evident.
4. **Descriptive test names** — State the behavior and condition, for example `it('shows an error when login fails', ...)`, rather than describing implementation steps.
5. **Test user-visible behavior** — For React components, use React Testing Library and query elements by accessible role and name, label, or text. Prefer `userEvent` for user interactions; use `fireEvent` only when a lower-level event is specifically needed. Avoid querying internal implementation details, CSS classes, or test IDs when an accessible query is available.
6. **Exercise realistic flows** — Prefer rendering the real component and exercising it through the UI. Mock only boundaries that should be isolated, such as network calls, navigation, or external libraries; avoid mocking the behavior under test or replacing large parts of the component tree unnecessarily.
7. **Reusable setup and test data** — Reuse existing test setup and shared helpers. Create small typed test-data builders or fixtures when setup is repeated; keep test data explicit and minimal. Avoid copying large setup blocks across tests.
8. **Parametrize related cases** — Use Vitest's `it.each` or `test.each` when the same behavior should be verified for multiple inputs or outcomes. Use descriptive case values and include meaningful edge cases without obscuring failures.
9. **Async behavior** — Await `userEvent` interactions. Use `findBy*` for elements that appear asynchronously and `waitFor` when waiting for an assertion or state transition that has no suitable `findBy*` query. Do not add arbitrary sleeps.
10. **Mock lifecycle** — Use `vi.fn`, `vi.mock`, and `vi.spyOn` only where appropriate. Reset or restore mocks between tests using the repository's established lifecycle patterns so cases remain independent.
11. **Assert outcomes** — Check visible output, callbacks, navigation, requests, or relevant state changes. Avoid asserting incidental implementation details or using snapshots as a substitute for behavior-focused assertions.
12. **Follow project tooling** — Use Vitest globals and the configured `happy-dom` environment from `frontend/vitest.config.ts`. Run focused tests from `frontend/` with `npm run test:run -- <test-file>`.

## Example

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import RatingBox from './RatingBox';
import { FlashcardRating } from '../../constants';

describe('RatingBox', () => {
  it('reports the selected rating when the user clicks a rating button', async () => {
    // GIVEN: A rating box with a callback.
    const user = userEvent.setup();
    const handleRate = vi.fn();
    render(<RatingBox handleRate={handleRate} />);

    // WHEN: The user selects Easy.
    await user.click(screen.getByRole('button', { name: 'Easy' }));

    // THEN: The callback receives the Easy rating.
    expect(handleRate).toHaveBeenCalledWith(FlashcardRating.EASY);
  });
});
```

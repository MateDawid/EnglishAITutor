import { describe, it, expect } from 'vitest';

import { SingleFlashcardModal } from './index';
import SingleFlashcardModalDefault from './SingleFlashcardModal';

describe('SingleFlashcardModal index exports', () => {
  it('re-exports SingleFlashcardModal as named export', () => {
    expect(SingleFlashcardModal).toBe(SingleFlashcardModalDefault);
  });
});

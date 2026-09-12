import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import type { ReactNode } from 'react';

import SingleFlashcardModal from './SingleFlashcardModal';
import type { Flashcard } from '../../types';

type StyledModalProps = {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
};

const testFlashcard: Flashcard = {
  id: '1',
  word: 'serendipity',
  meaning: 'finding valuable things by chance',
  part_of_speech: 'noun',
  example: 'A lucky serendipity brought them together.',
  rating: 'new',
};

vi.mock('../styles', () => ({
  StyledModal: ({ open, onClose, children }: StyledModalProps) => (
    <div data-testid="styled-modal" data-open={String(open)}>
      <button type="button" onClick={onClose}>
        close-from-modal
      </button>
      {open && children}
    </div>
  ),
}));

vi.mock('./FlashcardPaper', () => ({
  default: ({
    cardReversed,
    handleClose,
  }: {
    flashcard: Flashcard;
    cardReversed: boolean;
    setCardReversed: (reversed: boolean) => void;
    handleClose: (ratingChanged?: boolean) => void;
    setRefreshTimestamp: (timestamp: number | null) => void;
  }) => (
    <div data-testid="styled-paper" data-reversed={String(cardReversed)}>
      <button type="button" onClick={() => handleClose(false)}>
        close-from-back
      </button>
    </div>
  ),
}));

describe('SingleFlashcardModal', () => {
  const setOpen = vi.fn();
  const setRefreshTimestamp = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders in open state when flashcard is present', () => {
    render(
      <SingleFlashcardModal
        flashcard={testFlashcard}
        open={true}
        setOpen={setOpen}
        setRefreshTimestamp={setRefreshTimestamp}
      />
    );

    expect(screen.getByTestId('styled-modal')).toHaveAttribute('data-open', 'true');
    expect(screen.getByTestId('styled-paper')).toHaveAttribute('data-reversed', 'false');
  });

  it('renders closed state when open is false', () => {
    render(
      <SingleFlashcardModal
        flashcard={testFlashcard}
        open={false}
        setOpen={setOpen}
        setRefreshTimestamp={setRefreshTimestamp}
      />
    );

    expect(screen.getByTestId('styled-modal')).toHaveAttribute('data-open', 'false');
  });

  it('calls setOpen with false when modal onClose is triggered', () => {
    render(
      <SingleFlashcardModal
        flashcard={testFlashcard}
        open={true}
        setOpen={setOpen}
        setRefreshTimestamp={setRefreshTimestamp}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: 'close-from-modal' }));
    expect(setOpen).toHaveBeenCalledWith(false);
  });

  it('calls handleClose when close-from-back button is triggered', () => {
    render(
      <SingleFlashcardModal
        flashcard={testFlashcard}
        open={true}
        setOpen={setOpen}
        setRefreshTimestamp={setRefreshTimestamp}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: 'close-from-back' }));
    expect(setOpen).toHaveBeenCalledWith(false);
  });
});

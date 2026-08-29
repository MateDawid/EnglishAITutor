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

type StyledPaperProps = {
  reversed: boolean;
  children: ReactNode;
};

const testFlashcard: Flashcard = {
  word: 'serendipity',
  meaning: 'finding valuable things by chance',
  part_of_speech: 'noun',
  example: 'A lucky serendipity brought them together.',
};

vi.mock('./styles', () => ({
  StyledModal: ({ open, onClose, children }: StyledModalProps) => (
    <div data-testid="styled-modal" data-open={String(open)}>
      <button type="button" onClick={onClose}>
        close-from-modal
      </button>
      {children}
    </div>
  ),
  StyledPaper: ({ reversed, children }: StyledPaperProps) => (
    <div data-testid="styled-paper" data-reversed={String(reversed)}>
      {children}
    </div>
  ),
}));

vi.mock('./FlashcardFront', () => ({
  default: ({
    setCardReversed,
  }: {
    flashcard: Flashcard;
    setCardReversed: (reversed: boolean) => void;
  }) => (
    <button type="button" onClick={() => setCardReversed(true)}>
      reveal
    </button>
  ),
}));

vi.mock('./FlashcardBack', () => ({
  default: ({
    handleClose,
  }: {
    flashcard: Flashcard;
    handleClose: () => void;
  }) => (
    <button type="button" onClick={handleClose}>
      close-from-back
    </button>
  ),
}));

describe('SingleFlashcardModal', () => {
  const setOpen = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders in open state when flashcard is present', () => {
    render(<SingleFlashcardModal flashcard={testFlashcard} open={true} setOpen={setOpen} />);

    expect(screen.getByTestId('styled-modal')).toHaveAttribute('data-open', 'true');
    expect(screen.getByRole('button', { name: 'reveal' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'close-from-back' })).toBeInTheDocument();
  });

  it('forces closed state when flashcard is null', () => {
    render(<SingleFlashcardModal flashcard={null} open={true} setOpen={setOpen} />);

    expect(screen.getByTestId('styled-modal')).toHaveAttribute('data-open', 'false');
    expect(screen.queryByRole('button', { name: 'reveal' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'close-from-back' })).not.toBeInTheDocument();
  });

  it('closes and resets reversed state when modal onClose is triggered', () => {
    render(<SingleFlashcardModal flashcard={testFlashcard} open={true} setOpen={setOpen} />);

    fireEvent.click(screen.getByRole('button', { name: 'reveal' }));
    expect(screen.getByTestId('styled-paper')).toHaveAttribute('data-reversed', 'true');

    fireEvent.click(screen.getByRole('button', { name: 'close-from-modal' }));
    expect(setOpen).toHaveBeenCalledWith(false);
    expect(screen.getByTestId('styled-paper')).toHaveAttribute('data-reversed', 'false');
  });

  it('closes and resets reversed state when back close handler is triggered', () => {
    render(<SingleFlashcardModal flashcard={testFlashcard} open={true} setOpen={setOpen} />);

    fireEvent.click(screen.getByRole('button', { name: 'reveal' }));
    expect(screen.getByTestId('styled-paper')).toHaveAttribute('data-reversed', 'true');

    fireEvent.click(screen.getByRole('button', { name: 'close-from-back' }));
    expect(setOpen).toHaveBeenCalledWith(false);
    expect(screen.getByTestId('styled-paper')).toHaveAttribute('data-reversed', 'false');
  });
});

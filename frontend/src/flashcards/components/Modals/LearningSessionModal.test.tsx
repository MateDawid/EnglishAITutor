import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import type { ReactNode } from 'react';

import LearningSessionModal from './LearningSessionModal';
import type { Flashcard } from '../../types';

type StyledModalProps = {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
};

type StyledPaginationProps = {
  count: number;
  page: number;
  onChange: (event: unknown, page: number) => void;
  children?: ReactNode;
  renderItem?: (item: unknown) => ReactNode;
};

const mockFlashcards: Flashcard[] = [
  {
    id: '1',
    word: 'serendipity',
    meaning: 'finding valuable things by chance',
    part_of_speech: 'noun',
    example: 'A lucky serendipity brought them together.',
    rating: 'new',
  },
  {
    id: '2',
    word: 'eloquent',
    meaning: 'fluent and persuasive speaking',
    part_of_speech: 'adjective',
    example: 'Her eloquent speech moved the audience.',
    rating: 'learning',
  },
  {
    id: '3',
    word: 'ephemeral',
    meaning: 'lasting a very short time',
    part_of_speech: 'adjective',
    example: 'The beauty of cherry blossoms is ephemeral.',
    rating: 'known',
  },
];

const { mockApiGet } = vi.hoisted(() => ({
  mockApiGet: vi.fn(),
}));

vi.mock('../../../core/apiClient', () => ({
  default: {
    get: mockApiGet,
  },
}));

vi.mock('../../../core/store/AlertContext', () => ({
  useAlertContext: () => ({
    setAlert: vi.fn(),
  }),
}));

vi.mock('../styles', () => ({
  StyledModal: ({ open, onClose, children }: StyledModalProps) => (
    <div data-testid="styled-modal" data-open={String(open)}>
      <button type="button" onClick={onClose}>
        close-modal
      </button>
      {open && children}
    </div>
  ),
}));

vi.mock('./LearningSessionModal.styles', () => ({
  StyledPagination: ({
    count,
    page,
    onChange,
    renderItem,
  }: StyledPaginationProps) => (
    <div data-testid="pagination">
      <div>Page {page} of {count}</div>
      {renderItem && Array.from({ length: count }, (_, i) => (
        <div key={i}>
          {renderItem({ page: i + 1 })}
        </div>
      ))}
      <button
        type="button"
        onClick={() => onChange(null, page > 1 ? page - 1 : page)}
      >
        prev
      </button>
      <button
        type="button"
        onClick={() => onChange(null, page < count ? page + 1 : page)}
      >
        next
      </button>
    </div>
  ),
  StyledPaginationItem: ({
    page,
  }: {
    page?: number;
  }) => (
    page ? <span data-testid={`pagination-item-${page}`}>{page}</span> : null
  ),
}));

vi.mock('./FlashcardPaper', () => ({
  default: ({
    flashcard,
    cardReversed,
    handleClose,
  }: {
    flashcard: Flashcard;
    cardReversed: boolean;
    handleClose: (ratingChanged: boolean) => void;
  }) => (
    <div data-testid="flashcard-paper">
      <div>{flashcard.word}</div>
      <div>{cardReversed ? flashcard.meaning : 'Click to reveal'}</div>
      <button
        type="button"
        onClick={() => handleClose(false)}
      >
        close-card
      </button>
    </div>
  ),
}));

describe('LearningSessionModal', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockApiGet.mockResolvedValue({
      data: {
        items: mockFlashcards,
      },
    });
  });

  it('does not render modal when flashcards are not loaded and open is false', () => {
    render(<LearningSessionModal open={false} setOpen={vi.fn()} />);
    expect(screen.queryByTestId('styled-modal')).not.toBeInTheDocument();
  });

  it('fetches flashcards when modal opens', async () => {
    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(mockApiGet).toHaveBeenCalledWith('/flashcards/?page=1&page_size=10');
    });
  });

  it('does not fetch flashcards when modal is closed', () => {
    const { rerender } = render(<LearningSessionModal open={false} setOpen={vi.fn()} />);

    expect(mockApiGet).not.toHaveBeenCalled();

    rerender(<LearningSessionModal open={true} setOpen={vi.fn()} />);
    expect(mockApiGet).toHaveBeenCalled();
  });

  it('renders flashcard paper with first flashcard when flashcards are loaded', async () => {
    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByTestId('flashcard-paper')).toBeInTheDocument();
      expect(screen.getByText('serendipity')).toBeInTheDocument();
    });
  });

  it('does not render styled-modal when flashcards array is empty', async () => {
    mockApiGet.mockResolvedValue({
      data: {
        items: [],
      },
    });

    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(mockApiGet).toHaveBeenCalled();
    });

    expect(screen.queryByTestId('styled-modal')).not.toBeInTheDocument();
  });

  it('shows pagination with correct count', async () => {
    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByText(/Page 1 of 3/)).toBeInTheDocument();
    });
  });

  it('moves to next flashcard when pagination is clicked', async () => {
    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByText('serendipity')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: 'next' }));

    expect(screen.getByText('eloquent')).toBeInTheDocument();
    expect(screen.getByText(/Page 2 of 3/)).toBeInTheDocument();
  });

  it('closes modal when last flashcard is closed without rating change', async () => {
    const setOpen = vi.fn();
    render(<LearningSessionModal open={true} setOpen={setOpen} />);

    await waitFor(() => {
      expect(screen.getByTestId('flashcard-paper')).toBeInTheDocument();
    });

    // Navigate to last card
    fireEvent.click(screen.getByRole('button', { name: 'next' }));
    fireEvent.click(screen.getByRole('button', { name: 'next' }));

    expect(screen.getByText('ephemeral')).toBeInTheDocument();

    // Close the last card
    fireEvent.click(screen.getByRole('button', { name: 'close-card' }));

    expect(setOpen).toHaveBeenCalledWith(false);
  });

  it('moves to next flashcard when close-card is clicked on non-last card', async () => {
    const setOpen = vi.fn();
    render(<LearningSessionModal open={true} setOpen={setOpen} />);

    await waitFor(() => {
      expect(screen.getByText('serendipity')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: 'close-card' }));

    expect(screen.getByText('eloquent')).toBeInTheDocument();
    expect(setOpen).not.toHaveBeenCalled();
  });

  it('handles API error gracefully', async () => {
    mockApiGet.mockRejectedValue(new Error('API Error'));

    render(<LearningSessionModal open={true} setOpen={vi.fn()} />);

    await waitFor(() => {
      expect(mockApiGet).toHaveBeenCalled();
    });

    // Modal should not render when there's an error (no flashcards)
    expect(screen.queryByTestId('flashcard-paper')).not.toBeInTheDocument();
  });
});

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import type { ReactNode } from 'react';

import FlashcardBack from './FlashcardBack';
import type { Flashcard } from '../../types';

type WrapperProps = { children: ReactNode };
type ChipProps = { label: string };

const hoisted = vi.hoisted(() => ({
  mockExampleBox: vi.fn(({ example }: { example: string }) => <div data-testid="example-box">{example}</div>),
  mockRatingBox: vi.fn(({ handleRate }: { handleRate: (rating: number) => Promise<void> }) => (
    <button type="button" onClick={() => handleRate(1)}>
      rating-close
    </button>
  )),
  mockApiClient: {
    post: vi.fn(),
  },
}));

vi.mock('./styles', () => ({
  PaperBack: ({ children }: WrapperProps) => <div>{children}</div>,
  CardBox: ({ children }: WrapperProps) => <div>{children}</div>,
  HeaderTypography: ({ children }: WrapperProps) => <h2>{children}</h2>,
  MeaningBox: ({ children }: WrapperProps) => <div>{children}</div>,
  MeaningTypography: ({ children }: WrapperProps) => <p>{children}</p>,
  WordBox: ({ children }: WrapperProps) => <div>{children}</div>,
  StyledChip: ({ label }: ChipProps) => <span>{label}</span>,
}));

vi.mock('./ExampleBox', () => ({
  default: hoisted.mockExampleBox,
}));

vi.mock('./RatingBox', () => ({
  default: hoisted.mockRatingBox,
}));

vi.mock('../../../core/apiClient', () => ({
  default: hoisted.mockApiClient,
}));

const baseFlashcard: Flashcard = {
  word: 'meticulous',
  meaning: 'showing great attention to detail',
  part_of_speech: 'adjective',
  example: 'She kept meticulous notes.',
};

describe('FlashcardBack', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    hoisted.mockApiClient.post.mockResolvedValue({
      status: 201,
      data: { rating_changed: true },
    });
  });

  it('renders flashcard details and example when provided', () => {
    render(<FlashcardBack flashcard={baseFlashcard} handleClose={vi.fn()} setRefreshTimestamp={vi.fn()} />);

    expect(screen.getByText('meticulous')).toBeInTheDocument();
    expect(screen.getByText('adjective')).toBeInTheDocument();
    expect(screen.getByText('showing great attention to detail')).toBeInTheDocument();
    expect(screen.getByTestId('example-box')).toHaveTextContent('She kept meticulous notes.');
    expect(hoisted.mockExampleBox).toHaveBeenCalledWith(
      expect.objectContaining({ example: 'She kept meticulous notes.' }),
      undefined,
    );
  });

  it('does not render example when flashcard example is null', () => {
    render(
      <FlashcardBack
        flashcard={{ ...baseFlashcard, example: null }}
        handleClose={vi.fn()}
        setRefreshTimestamp={vi.fn()}
      />,
    );

    expect(screen.queryByTestId('example-box')).not.toBeInTheDocument();
    expect(hoisted.mockExampleBox).not.toHaveBeenCalled();
  });

  it('passes close handler to RatingBox and closes on rating action', async () => {
    const handleClose = vi.fn();

    render(<FlashcardBack flashcard={baseFlashcard} handleClose={handleClose} setRefreshTimestamp={vi.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: 'rating-close' }));

    expect(hoisted.mockRatingBox).toHaveBeenCalled();
    
    await waitFor(() => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });
  });
});

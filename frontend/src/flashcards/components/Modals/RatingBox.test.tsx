import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import type { ReactNode } from 'react';

import RatingBox from './RatingBox';
import { FlashcardRating } from '../../constants';

type WrapperProps = { children: ReactNode };

type ButtonProps = {
  children: ReactNode;
  onClick: () => void;
};

vi.mock('./RatingBox.styles', () => ({
  StyledRatingBox: ({ children }: WrapperProps) => <section>{children}</section>,
  ButtonsBox: ({ children }: WrapperProps) => <div>{children}</div>,
  EasyButton: ({ children, onClick }: ButtonProps) => (
    <button type="button" onClick={onClick}>
      {children}
    </button>
  ),
  MediumButton: ({ children, onClick }: ButtonProps) => (
    <button type="button" onClick={onClick}>
      {children}
    </button>
  ),
  HardButton: ({ children, onClick }: ButtonProps) => (
    <button type="button" onClick={onClick}>
      {children}
    </button>
  ),
}));

describe('RatingBox', () => {
  const handleRate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the rating prompt and buttons', () => {
    render(<RatingBox handleRate={handleRate} />);

    expect(screen.getByText('How hard was this word for you?')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Easy' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Medium' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Hard' })).toBeInTheDocument();
  });

  it('calls handleRate with the correct rating when buttons are clicked', () => {
    render(<RatingBox handleRate={handleRate} />);

    fireEvent.click(screen.getByRole('button', { name: 'Easy' }));
    fireEvent.click(screen.getByRole('button', { name: 'Medium' }));
    fireEvent.click(screen.getByRole('button', { name: 'Hard' }));

    expect(handleRate).toHaveBeenNthCalledWith(1, FlashcardRating.EASY);
    expect(handleRate).toHaveBeenNthCalledWith(2, FlashcardRating.MEDIUM);
    expect(handleRate).toHaveBeenNthCalledWith(3, FlashcardRating.HARD);
  });
});

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import type { ReactNode } from 'react';

import RatingBox from './RatingBox';
import { EASY_RATING_VALUE, MEDIUM_RATING_VALUE, HARD_RATING_VALUE } from '../../constants';

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
  const handleClose = vi.fn();
  const logSpy = vi.spyOn(console, 'log').mockImplementation(() => undefined);

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    logSpy.mockClear();
  });

  it('renders the rating prompt and buttons', () => {
    render(<RatingBox handleClose={handleClose} />);

    expect(screen.getByText('How hard was this word for you?')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Easy' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Medium' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Hard' })).toBeInTheDocument();
  });

  it('logs selected difficulty and closes for each rating button', () => {
    render(<RatingBox handleClose={handleClose} />);

    fireEvent.click(screen.getByRole('button', { name: 'Easy' }));
    fireEvent.click(screen.getByRole('button', { name: 'Medium' }));
    fireEvent.click(screen.getByRole('button', { name: 'Hard' }));

    expect(logSpy).toHaveBeenNthCalledWith(1, `User rated the word as: ${EASY_RATING_VALUE}`);
    expect(logSpy).toHaveBeenNthCalledWith(2, `User rated the word as: ${MEDIUM_RATING_VALUE}`);
    expect(logSpy).toHaveBeenNthCalledWith(3, `User rated the word as: ${HARD_RATING_VALUE}`);
    expect(handleClose).toHaveBeenCalledTimes(3);
  });
});

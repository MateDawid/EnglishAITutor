import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import type { ReactNode } from 'react';

import FlashcardFront from './FlashcardFront';
import type { Flashcard } from '../../types';

type WrapperProps = { children: ReactNode };
type ChipProps = { label: string };
type RevealButtonProps = {
  children: ReactNode;
  onClick: () => void;
};

vi.mock('./styles', () => ({
  PaperFace: ({ children }: WrapperProps) => <div>{children}</div>,
  CardBox: ({ children }: WrapperProps) => <div>{children}</div>,
  HeaderTypography: ({ children }: WrapperProps) => <h2>{children}</h2>,
  WordTypography: ({ children }: WrapperProps) => <div>{children}</div>,
  WordBox: ({ children }: WrapperProps) => <div>{children}</div>,
  StyledChip: ({ label }: ChipProps) => <span>{label}</span>,
  RevealButton: ({ children, onClick }: RevealButtonProps) => (
    <button type="button" onClick={onClick}>
      {children}
    </button>
  ),
}));

const flashcard: Flashcard = {
  word: 'ephemeral',
  meaning: 'lasting for a short time',
  part_of_speech: 'adjective',
  example: 'The beauty of the sunset was ephemeral.',
};

describe('FlashcardFront', () => {
  it('renders flashcard front details', () => {
    render(<FlashcardFront flashcard={flashcard} setCardReversed={vi.fn()} />);

    expect(screen.getByText('Word')).toBeInTheDocument();
    expect(screen.getByText('ephemeral')).toBeInTheDocument();
    expect(screen.getByText('adjective')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Reveal' })).toBeInTheDocument();
  });

  it('sets reversed state to true when Reveal is clicked', () => {
    const setCardReversed = vi.fn();

    render(<FlashcardFront flashcard={flashcard} setCardReversed={setCardReversed} />);

    fireEvent.click(screen.getByRole('button', { name: 'Reveal' }));

    expect(setCardReversed).toHaveBeenCalledWith(true);
  });
});

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import FlashcardsPage from './FlashcardsPage';

vi.mock('../components/FlashcardsDataGrid', () => ({
  default: () => <div data-testid="flashcards-data-grid" />,
}));

describe('FlashcardsPage', () => {
  beforeEach(() => {
    document.title = 'Initial title';
  });

  it('renders flashcards heading and data grid', () => {
    render(<FlashcardsPage />);

    expect(screen.getByRole('heading', { name: 'Flashcards' })).toBeInTheDocument();
    expect(screen.getByTestId('flashcards-data-grid')).toBeInTheDocument();
  });

  it('sets document title on mount', async () => {
    render(<FlashcardsPage />);

    await waitFor(() => {
      expect(document.title).toBe('Flashcards');
    });
  });
});
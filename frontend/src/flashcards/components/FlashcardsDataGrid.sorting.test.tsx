import { describe, it, expect } from 'vitest';
import { formatSortModel } from './FlashcardsDataGrid.sorting';

describe('FlashcardsDataGrid.sorting', () => {
  it('returns empty object for empty sort model', () => {
    const result = formatSortModel([]);

    expect(result).toEqual({});
  });

  it('formats ascending sort model', () => {
    const result = formatSortModel([{ field: 'word', sort: 'asc' }]);

    expect(result).toEqual({ order_by: 'word' });
  });

  it('formats descending sort model with prefixed dash', () => {
    const result = formatSortModel([{ field: 'word', sort: 'desc' }]);

    expect(result).toEqual({ order_by: '-word' });
  });
});
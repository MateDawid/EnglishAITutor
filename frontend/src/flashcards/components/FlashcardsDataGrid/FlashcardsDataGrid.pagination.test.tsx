import { describe, it, expect } from 'vitest';
import { formatPaginationModel, PAGE_SIZE_OPTIONS } from './FlashcardsDataGrid.pagination';

describe('FlashcardsDataGrid.pagination', () => {
  it('exposes expected page size options', () => {
    expect(PAGE_SIZE_OPTIONS).toEqual([10, 20, 50]);
  });

  it('formats pagination model for API params', () => {
    const result = formatPaginationModel({ page: 0, pageSize: 20 });

    expect(result).toEqual({
      page: 1,
      page_size: 20,
    });
  });

  it('increments page correctly for non-zero pages', () => {
    const result = formatPaginationModel({ page: 3, pageSize: 50 });

    expect(result.page).toBe(4);
    expect(result.page_size).toBe(50);
  });
});
import { describe, it, expect, vi } from 'vitest';

vi.mock('@mui/x-data-grid', () => ({
  getGridStringOperators: () => [
    { value: 'contains' },
    { value: 'equals' },
    { value: 'startsWith' },
  ],
  getGridNumericOperators: () => [
    { value: '=' },
    { value: '>=' },
    { value: '<=' },
    { value: '>' },
  ],
  getGridSingleSelectOperators: () => [
    { value: 'is' },
    { value: 'not' },
  ],
}));

import {
  formatFilterModel,
  STRING_FILTER_OPERATORS,
  SINGLE_SELECT_FILTER_OPERATORS,
  NUMBER_FILTER_OPERATORS,
} from './FlashcardsDataGrid.filtering';

describe('FlashcardsDataGrid.filtering', () => {
  it('keeps only expected string operators', () => {
    expect(STRING_FILTER_OPERATORS.every((operator) => ['contains', 'equals'].includes(operator.value))).toBe(true);
    expect(STRING_FILTER_OPERATORS.some((operator) => operator.value === 'contains')).toBe(true);
    expect(STRING_FILTER_OPERATORS.some((operator) => operator.value === 'equals')).toBe(true);
  });

  it('keeps only expected single-select operators', () => {
    expect(SINGLE_SELECT_FILTER_OPERATORS.every((operator) => operator.value === 'is')).toBe(true);
  });

  it('keeps only expected numeric operators', () => {
    expect(NUMBER_FILTER_OPERATORS.every((operator) => ['=', '>=', '<='].includes(operator.value))).toBe(true);
  });

  it('returns empty object when there are no filter items', () => {
    const result = formatFilterModel({ items: [] });

    expect(result).toEqual({});
  });

  it('returns empty object when first filter item has null value', () => {
    const result = formatFilterModel({
      items: [{ field: 'word', operator: 'contains', value: null }],
    });

    expect(result).toEqual({});
  });

  it('formats contains filter and strips surrounding quotes', () => {
    const result = formatFilterModel({
      items: [{ field: 'word', operator: 'contains', value: '"hello"' }],
    });

    expect(result).toEqual({ word: 'hello' });
  });

  it('formats equals filter as quoted value and strips extra surrounding quotes', () => {
    const result = formatFilterModel({
      items: [{ field: 'word', operator: 'equals', value: '"hello"' }],
    });

    expect(result).toEqual({ word: '"hello"' });
  });

  it('returns raw field-value object for unhandled operators', () => {
    const result = formatFilterModel({
      items: [{ field: 'part_of_speech', operator: 'is', value: 'noun' }],
    });

    expect(result).toEqual({ part_of_speech: 'noun' });
  });
});
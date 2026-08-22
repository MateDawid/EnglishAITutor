import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, waitFor, act } from '@testing-library/react';
import type { ReactNode } from 'react';
import FlashcardsDataGrid from './FlashcardsDataGrid';
import { useMediaQuery } from '@mui/material';
import { formatPaginationModel } from './FlashcardsDataGrid.pagination';
import { formatSortModel } from './FlashcardsDataGrid.sorting';
import { formatFilterModel } from './FlashcardsDataGrid.filtering';
import { ALL_COLUMNS, MINIMUM_COLUMNS } from './FlashcardsDataGrid.columns';

type TestPaginationModel = { page: number; pageSize: number };
type TestSortItem = { field: string; sort: 'asc' | 'desc' | null | undefined };
type TestFilterItem = { field: string; operator: string; value: unknown };
type TestFilterModel = { items: TestFilterItem[] };

type TestDataGridProps = {
  rows: unknown[];
  rowCount: number;
  loading: boolean;
  columns: unknown[];
  onPaginationModelChange: (model: TestPaginationModel) => void;
  onSortModelChange: (model: TestSortItem[]) => void;
  onFilterModelChange: (model: TestFilterModel) => void;
};

const hoisted = vi.hoisted(() => ({
  mockGet: vi.fn(),
  mockSetAlert: vi.fn(),
  latestDataGridProps: undefined as TestDataGridProps | undefined,
}));

vi.mock('../../core/apiClient', () => ({
  default: {
    get: hoisted.mockGet,
  },
}));

vi.mock('../../core/store/AlertContext', () => ({
  useAlertContext: () => ({
    setAlert: hoisted.mockSetAlert,
  }),
}));

vi.mock('./FlashcardsDataGrid.styles', () => ({
  StyledBox: ({ children }: { children: ReactNode }) => <div data-testid="grid-box">{children}</div>,
  StyledDataGrid: (props: TestDataGridProps) => {
    hoisted.latestDataGridProps = props;
    return <div data-testid="grid" />;
  },
}));

vi.mock('./FlashcardsDataGrid.columns', () => ({
  ALL_COLUMNS: [{ field: 'all-column' }],
  MINIMUM_COLUMNS: [{ field: 'minimum-column' }],
}));

vi.mock('./FlashcardsDataGrid.pagination', () => ({
  PAGE_SIZE_OPTIONS: [10, 20, 50],
  formatPaginationModel: vi.fn((model) => ({
    page: model.page + 1,
    page_size: model.pageSize,
  })),
}));

vi.mock('./FlashcardsDataGrid.sorting', () => ({
  formatSortModel: vi.fn((model) => {
    if (model.length === 0) {
      return {};
    }
    const sortItem = model[0];
    return { order_by: sortItem.sort === 'desc' ? `-${sortItem.field}` : sortItem.field };
  }),
}));

vi.mock('./FlashcardsDataGrid.filtering', () => ({
  formatFilterModel: vi.fn((model) => {
    if (!model.items.length) {
      return {};
    }
    const item = model.items[0];
    if (item.value == null) {
      return {};
    }
    return { [item.field]: item.value };
  }),
}));

vi.mock('@mui/material', async () => {
  const actual = await vi.importActual<typeof import('@mui/material')>('@mui/material');
  return {
    ...actual,
    useMediaQuery: vi.fn(),
  };
});

describe('FlashcardsDataGrid', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    hoisted.latestDataGridProps = undefined;
    vi.mocked(useMediaQuery).mockReturnValue(false);
    hoisted.mockGet.mockResolvedValue({
      data: {
        items: [{ id: 1, word: 'alpha' }],
        total: 1,
      },
    });
  });

  it('loads flashcards and passes fetched data to DataGrid', async () => {
    render(<FlashcardsDataGrid />);

    await waitFor(() => {
      expect(hoisted.mockGet).toHaveBeenCalledWith('/flashcards/', {
        params: {
          page: 1,
          page_size: 10,
        },
      });
    });

    await waitFor(() => {
      expect(hoisted.latestDataGridProps.rows).toEqual([{ id: 1, word: 'alpha' }]);
      expect(hoisted.latestDataGridProps.rowCount).toBe(1);
      expect(hoisted.latestDataGridProps.loading).toBe(false);
      expect(hoisted.latestDataGridProps.columns).toBe(MINIMUM_COLUMNS);
    });
  });

  it('uses all columns on medium and larger screens', async () => {
    vi.mocked(useMediaQuery).mockReturnValue(true);

    render(<FlashcardsDataGrid />);

    await waitFor(() => {
      expect(hoisted.latestDataGridProps.columns).toBe(ALL_COLUMNS);
    });
  });

  it('shows alert when loading flashcards fails', async () => {
    hoisted.mockGet.mockRejectedValueOnce(new Error('Network error'));

    render(<FlashcardsDataGrid />);

    await waitFor(() => {
      expect(hoisted.mockSetAlert).toHaveBeenCalledWith({
        type: 'error',
        message: 'Failed to load Flashcards.',
      });
    });

    expect(hoisted.latestDataGridProps.loading).toBe(false);
  });

  it('refetches data when pagination, sorting, and filtering change', async () => {
    render(<FlashcardsDataGrid />);

    await waitFor(() => {
      expect(hoisted.mockGet).toHaveBeenCalledTimes(1);
    });

    act(() => {
      hoisted.latestDataGridProps.onPaginationModelChange({ page: 1, pageSize: 20 });
    });
    await waitFor(() => {
      expect(formatPaginationModel).toHaveBeenLastCalledWith({ page: 1, pageSize: 20 });
    });

    act(() => {
      hoisted.latestDataGridProps.onSortModelChange([{ field: 'word', sort: 'desc' }]);
    });
    await waitFor(() => {
      expect(formatSortModel).toHaveBeenLastCalledWith([{ field: 'word', sort: 'desc' }]);
    });

    act(() => {
      hoisted.latestDataGridProps.onFilterModelChange({
        items: [{ field: 'word', operator: 'contains', value: 'alp' }],
      });
    });
    await waitFor(() => {
      expect(formatFilterModel).toHaveBeenLastCalledWith({
        items: [{ field: 'word', operator: 'contains', value: 'alp' }],
      });
    });

    await waitFor(() => {
      expect(hoisted.mockGet).toHaveBeenCalledTimes(4);
    });
  });
});
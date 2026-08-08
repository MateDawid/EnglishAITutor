import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import { useTheme, useMediaQuery } from '@mui/material';
import { formatPaginationModel, PAGE_SIZE_OPTIONS } from './FlashcardsDataGrid.pagination';
import { mappedFilterOperators, formatFilterModel } from './FlashcardsDataGrid.filtering';
import { StyledDataGrid } from './FlashcardsDataGrid.styles';
import apiClient from '../../core/apiClient';
import { useAlertContext } from '../../core/store/AlertContext';
import type { GridPaginationModel, GridSortModel, GridColDef } from '@mui/x-data-grid';
import { formatSortModel } from './FlashcardsDataGrid.sorting';

const COLUMNS: GridColDef[] = [
  {
    field: 'word',
    type: 'string',
    headerName: 'Word',
    headerAlign: 'left',
    align: 'left',
    flex: 1,
    filterable: true,
    sortable: true,
  },
  {
    field: 'part_of_speech',
    type: 'singleSelect',
    headerName: 'Part of speech',
    headerAlign: 'left',
    align: 'left',
    flex: 1,
    filterable: true,
    sortable: false,
    // TODO - add valueOptions dynamically from API instead of hardcoding them here
    valueOptions: ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection'],
  },
  {
    field: 'meaning',
    type: 'string',
    headerName: 'Meaning',
    headerAlign: 'left',
    align: 'left',
    flex: 3,
    filterable: true,
    sortable: false,
  }
];


/**
 * DataTable component for displaying DataGrid with data fetched from API.
 * @param {object} props
 * @param {number} props.transferType - Type of Transfer. Options: TransferTypes.INCOME, TransferTypes.EXPENSE.
 */
const FlashcardsDataGrid = () => {
  const theme = useTheme();
  const isMdUp = useMediaQuery(theme.breakpoints.up('md'));
  // Contexts
  const { setAlert } = useAlertContext();

  // Data rows
  const [rows, setRows] = useState([]);
  const [rowCount, setRowCount] = useState(0);

  // Loading and pagination
  const [loading, setLoading] = useState(true);
  const [paginationModel, setPaginationModel] = React.useState<GridPaginationModel>({
    pageSize: PAGE_SIZE_OPTIONS[0],
    page: 0,
  });

  // Filtering and sorting
  const [sortModel, setSortModel] = React.useState<GridSortModel>([]);
  const [filterModel, setFilterModel] = React.useState({ items: [] });

  // const extendedColumns = [
  //   // Map column type to proper filter operators
  //   ...COLUMNS.map((column) => ({
  //     ...column,
  //     filterOperators:
  //       column.type && column.type in mappedFilterOperators
  //         ? mappedFilterOperators[column.type]
  //         : undefined,
  //   })),
  // ];

  const responsiveColumns = isMdUp ? COLUMNS : [COLUMNS[0], COLUMNS[2]];

  /**
   * Fetches objects list from API.
   */
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get(
          '/flashcards/',
          {
            params: {
              ...formatPaginationModel(paginationModel),
              ...formatSortModel(sortModel),
              ///...formatFilterModel(filterModel, extendedColumns),
            }
          }
        );
        setRows(response.data.items);
        setRowCount(response.data.total);
      } catch {
        setAlert({
          type: 'error',
          message: `Failed to load Flashcards.`,
        });
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [paginationModel, sortModel, filterModel]);

  /**
   * Function to update DataGrid pagination model.
   * @param {GridPaginationModel} updatedPaginationModel - Updated pagination model.
   */
  function updatePagination(updatedPaginationModel: GridPaginationModel) {
    setPaginationModel(updatedPaginationModel);
  }

  /**
   * Function to update DataGrid sort model.
   * @param {GridSortModel} updatedSortModel - Updated sort model.
   */
  function updateSorting(updatedSortModel: GridSortModel) {
    setSortModel(updatedSortModel);
  }

  /**
   * Function to update DataGrid filter model.
   * @param {object} updatedFilterModel - Updated filter model.
   */
  function updateFiltering(updatedFilterModel) {
    setFilterModel(updatedFilterModel);
  }

  return (
    <Box
      sx={{
        flexGrow: 1,
        marginTop: 2,
        width: '100%',
        maxWidth: '100%',
        height: 600,
      }}
    >
      <StyledDataGrid
        rows={rows}
        columns={responsiveColumns}
        loading={loading}
        rowCount={rowCount}
        paginationMode="server"
        paginationModel={paginationModel}
        onPaginationModelChange={updatePagination}
        pageSizeOptions={PAGE_SIZE_OPTIONS}
        sortingMode="server"
        onSortModelChange={updateSorting}
        filterMode="server"
        filterModel={filterModel}
        onFilterModelChange={updateFiltering}
        disableColumnResize={true}
        disableRowSelectionOnClick
      />
    </Box>
  );
};

export default FlashcardsDataGrid;

import React, { useEffect, useState, type JSX } from 'react';
import Box from '@mui/material/Box';
import { useTheme, useMediaQuery } from '@mui/material';
import { formatPaginationModel, PAGE_SIZE_OPTIONS } from './FlashcardsDataGrid.pagination';
import { formatFilterModel } from './FlashcardsDataGrid.filtering';
import { StyledDataGrid } from './FlashcardsDataGrid.styles';
import apiClient from '../../core/apiClient';
import { useAlertContext } from '../../core/store/AlertContext';
import type { GridPaginationModel, GridSortModel, GridFilterModel } from '@mui/x-data-grid';
import { formatSortModel } from './FlashcardsDataGrid.sorting';
import { ALL_COLUMNS, MINIMUM_COLUMNS } from './FlashcardsDataGrid.columns';


/**
 * FlashcardsDataGrid component for displaying DataGrid with Flashcards fetched from API.
 * @return {JSX.Element} - Rendered component.
 */
const FlashcardsDataGrid = (): JSX.Element => {
  // Theme
  const theme = useTheme();
  const isMdUp = useMediaQuery(theme.breakpoints.up('md'));
  // Contexts
  const { setAlert } = useAlertContext();
  // Data
  const columns = isMdUp ? ALL_COLUMNS : MINIMUM_COLUMNS;
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
  const [filterModel, setFilterModel] = React.useState<GridFilterModel>({ items: [] });

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
              ...formatFilterModel(filterModel),
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
   * @param {GridFilterModel} updatedFilterModel - Updated filter model.
   */
  function updateFiltering(updatedFilterModel: GridFilterModel) {
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
        columns={columns}
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

import React, { useEffect, useState, type JSX } from 'react';
import { useTheme, useMediaQuery } from '@mui/material';
import { formatPaginationModel, PAGE_SIZE_OPTIONS } from './FlashcardsDataGrid.pagination';
import { formatFilterModel } from './FlashcardsDataGrid.filtering';
import { StyledBox, StyledDataGrid } from './FlashcardsDataGrid.styles';
import type { GridPaginationModel, GridSortModel, GridFilterModel } from '@mui/x-data-grid';
import { formatSortModel } from './FlashcardsDataGrid.sorting';
import { ALL_COLUMNS, MINIMUM_COLUMNS } from './FlashcardsDataGrid.columns';
import { useAlertContext } from '../../../core/store/AlertContext';
import apiClient from '../../../core/apiClient';
import SingleFlashcardModal from '../SingleFlashcardModal';

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
  // Modal state
  const [open, setOpen] = useState(false);
  const [openedFlashcard, setOpenedFlashcard] = useState({});

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
    <StyledBox>
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
        onRowClick={(params) => {
          setOpenedFlashcard(params.row);
          setOpen(true);
        }}
      />
      <SingleFlashcardModal
        flashcard={openedFlashcard}
        open={open}
        setOpen={setOpen}
      />
    </StyledBox>
  );
};

export default FlashcardsDataGrid;

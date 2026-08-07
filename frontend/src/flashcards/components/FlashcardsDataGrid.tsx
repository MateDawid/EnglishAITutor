import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';

import { useTheme, useMediaQuery } from '@mui/material';
import { styled } from '@mui/material/styles';
import { DataGrid } from '@mui/x-data-grid';
import { useAlertContext } from '../../core/store/AlertContext';
import apiClient from "../../core/apiClient";


const pageSizeOptions = [10, 50, 100];

const StyledDataGrid = styled(DataGrid)(() => ({
  minWidth: '100%',
  maxWidth: '100%',
  border: 0,
  '& .MuiDataGrid-columnHeaderTitle, .MuiTablePagination-selectLabel, .MuiTablePagination-select, .MuiTablePagination-displayedRows':
    { fontWeight: 'bold' },
  '& .MuiDataGrid-cell': {
    borderRight: '1px solid #303030',
    borderRightColor: '#f0f0f0',
  },
  '& .MuiDataGrid-columnsContainer, .MuiDataGrid-cell, .MuiDataGrid-footerContainer':
  {
    borderBottom: '#f0f0f0',
  },
}));

import {
  getGridDateOperators,
  getGridStringOperators,
  getGridNumericOperators,
  getGridBooleanOperators,
  getGridSingleSelectOperators,
} from '@mui/x-data-grid';

/**
 * Mapping of DataGrid columns types with supported filter methods.
 */
export const mappedFilterOperators = {
  string: getGridStringOperators().filter((operator) =>
    ['contains'].includes(operator.value)
  ),
  date: getGridDateOperators().filter((operator) =>
    ['is', 'before', 'onOrBefore', 'after', 'onOrAfter'].includes(
      operator.value
    )
  ),
  dateTime: getGridDateOperators(true).filter((operator) =>
    ['is', 'before', 'onOrBefore', 'after', 'onOrAfter'].includes(
      operator.value
    )
  ),
  number: getGridNumericOperators().filter((operator) =>
    ['=', '>=', '<='].includes(operator.value)
  ),
  boolean: getGridBooleanOperators(),
  singleSelect: getGridSingleSelectOperators().filter((operator) =>
    ['is'].includes(operator.value)
  ),
};

/**
 * Function for formatting filterModel for API calls purposes.
 * @param {object} updatedFilterModel - Updated filterModel returned from DataGrid after update.
 * @param {object} columns - Displayed columns settings.
 * @return {object} - Formatted filterModel for DataGrid.
 */
export function formatFilterModel(updatedFilterModel, columns) {
  if (updatedFilterModel.items.length === 0) {
    return {};
  } else if (updatedFilterModel.items[0].value == null) {
    return {};
  }
  const filterItem = updatedFilterModel.items[0];
  const column = columns.find((column) => column.field === filterItem.field);
  switch (column.type) {
    case 'date':
      return formatDateFilter(filterItem);
    case 'number':
      return formatNumberFilter(filterItem);
    default:
      return { [filterItem.field]: filterItem.value };
  }
}

/**
 * Function for formatting date filter for API calls purposes.
 * @param {object} filterItem - Filter definition received from DataGrid
 * @return {object} - Formatted filterModel with date filter for DataGrid.
 */
function formatDateFilter(filterItem) {
  switch (filterItem.operator) {
    case 'is':
      return {
        [`${filterItem.field}_after`]: formatDate(filterItem.value),
        [`${filterItem.field}_before`]: formatDate(filterItem.value),
      };
    case 'before': {
      let dayBefore = new Date(filterItem.value);
      dayBefore.setDate(dayBefore.getDate() - 1);
      return { [`${filterItem.field}_before`]: formatDate(dayBefore) };
    }
    case 'onOrBefore':
      return { [`${filterItem.field}_before`]: formatDate(filterItem.value) };
    case 'after': {
      let dayAfter = new Date(filterItem.value);
      dayAfter.setDate(dayAfter.getDate() + 1);
      return { [`${filterItem.field}_after`]: formatDate(dayAfter) };
    }
    case 'onOrAfter':
      return { [`${filterItem.field}_after`]: formatDate(filterItem.value) };
    default:
      return { [filterItem.field]: filterItem.value };
  }
}

/**
 * Function for formatting Date object into string in format YYYY-MM-DD
 * @param {Date} date - Filter definition received from DataGrid
 * @return {string} - Formatted filterModel with date filter for DataGrid.
 */
function formatDate(date) {
  // TODO - use it in all places where formatting appears
  return date.toLocaleDateString('en-CA');
}

/**
 * Function for formatting number filter for API calls purposes.
 * @param {object} filterItem - Filter definition received from DataGrid
 * @return {object} - Formatted filterModel with number filter for DataGrid.
 */
function formatNumberFilter(filterItem) {
  switch (filterItem.operator) {
    case '>=': {
      return { [`${filterItem.field}_min`]: filterItem.value };
    }
    case '<=':
      return { [`${filterItem.field}_max`]: filterItem.value };
    default:
      return { [filterItem.field]: filterItem.value };
  }
}

/**
 * Function to prepare mapping of API ordering fields for DataTable columns other than column names.
 * @param {object} columns - DataTable columns definitions.
 * @return {object} - Mapping for sorting DataTable rows.
 */
const getSortFieldMapping = (columns) => {
  return columns.reduce((acc, column) => {
    if (column.sortField) {
      acc[column.field] = column.sortField;
    }
    return acc;
  }, {});
};



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
  const [paginationModel, setPaginationModel] = React.useState({
    pageSize: pageSizeOptions[0],
    page: 0,
  });

  // Filtering and sorting
  const [sortModel, setSortModel] = React.useState({});
  const [filterModel, setFilterModel] = React.useState({ items: [] });

  const columns = [
    {
      field: 'word',
      type: 'string',
      headerName: 'Word',
      headerAlign: 'center',
      align: 'center',
      flex: 2,
      filterable: true,
      sortable: true,
    },
    {
      field: 'meaning',
      type: 'string',
      headerName: 'Meaning',
      headerAlign: 'center',
      align: 'left',
      flex: 2,
      filterable: true,
      sortable: false,
    },
    {
      field: 'example',
      type: 'string',
      headerName: 'Example',
      headerAlign: 'center',
      align: 'left',
      flex: 2,
      filterable: true,
      sortable: false,
    },
    {
      field: 'part_of_speech',
      type: 'singleSelect',
      headerName: 'Part of speech',
      headerAlign: 'center',
      align: 'center',
      flex: 2,
      filterable: true,
      sortable: true,
      // TODO - add valueOptions dynamically from API instead of hardcoding them here
      valueOptions: ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection'],
    },
  ];

  const extendedColumns = [
    // Map column type to proper filter operators
    ...columns.map((column) => ({
      ...column,
      filterOperators:
        column.type in mappedFilterOperators
          ? mappedFilterOperators[column.type]
          : undefined,
    })),
  ];
  const sortFieldMapping = getSortFieldMapping(extendedColumns);

  /**
   * Fetches objects list from API.
   */
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get(
          '/flashcards/',
          // paginationModel,
          // sortModel,
          // formatFilterModel(filterModel, columns)
        );
        console.log(response);
        setRows(response.data.items);
        console.log(response.data.total);
        setRowCount(response.total);
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
   * @param {object} updatedPaginationModel - updated pagination model.
   */
  function updatePagination(updatedPaginationModel) {
    setPaginationModel(updatedPaginationModel);
  }

  /**
   * Function to update DataGrid sort model.
   * @param {Array} updatedSortModel - updated sort model.
   */
  function updateSorting(updatedSortModel) {
    if (updatedSortModel.length === 0) {
      setSortModel({});
    } else {
      const sortField =
        sortFieldMapping[updatedSortModel[0].field] ||
        updatedSortModel[0].field;
      setSortModel({
        ordering:
          updatedSortModel[0].sort === 'desc' ? '-' + sortField : sortField,
      });
    }
  }

  /**
   * Function to update DataGrid filter model.
   * @param {object} updatedFilterModel - updated filter model.
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
        columns={extendedColumns}
        // columns={
        //   isMdUp
        //     ? extendedColumns
        //     : [
        //       extendedColumns[0],
        //       extendedColumns[6],
        //       extendedColumns[extendedColumns.length - 1],
        //     ]
        // }
        loading={loading}
        rowCount={rowCount}
        paginationMode="server"
        paginationModel={paginationModel}
        onPaginationModelChange={updatePagination}
        pageSizeOptions={pageSizeOptions}
        sortingMode="server"
        onSortModelChange={updateSorting}
        filterMode="server"
        filterModel={filterModel}
        onFilterModelChange={updateFiltering}
        disableColumnResize={true}
        disableRowSelectionOnClick
        // slots={{
        //   pagination: FlashcardsDataGridFooter,
        // }}
        // slotProps={{
        //   pagination: {},
        // }}
      />
    </Box>
  );
};
export default FlashcardsDataGrid;

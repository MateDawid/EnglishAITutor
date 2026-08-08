import {
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
    case 'number':
      return formatNumberFilter(filterItem);
    default:
      return { [filterItem.field]: filterItem.value };
  }
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
export const getSortFieldMapping = (columns) => {
  return columns.reduce((acc, column) => {
    if (column.sortField) {
      acc[column.field] = column.sortField;
    }
    return acc;
  }, {});
};


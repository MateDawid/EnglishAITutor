import {
  getGridStringOperators,
  getGridNumericOperators,
  // getGridBooleanOperators,
  getGridSingleSelectOperators,
  type GridFilterModel,
} from '@mui/x-data-grid';

export const STRING_FILTER_OPERATORS = getGridStringOperators()
.filter((operator) =>
  ['contains', 'equals'].includes(operator.value)
)

export const SINGLE_SELECT_FILTER_OPERATORS = getGridSingleSelectOperators().filter((operator) =>
  ['is'].includes(operator.value)
)

export const NUMBER_FILTER_OPERATORS = getGridNumericOperators().filter((operator) =>
  ['=', '>=', '<='].includes(operator.value)
)

// export const BOOLEAN_FILTER_OPERATORS = getGridBooleanOperators()

/**
 * Function for formatting filterModel for API calls purposes.
 * @param {object} updatedFilterModel - Updated filterModel returned from DataGrid after update.
 * @return {object} - Formatted filterModel for API calls.
 */
export function formatFilterModel(updatedFilterModel: GridFilterModel): object {
  if (updatedFilterModel.items.length === 0) {
    return {};
  } else if (updatedFilterModel.items[0].value == null) {
    return {};
  }
  const filterItem = updatedFilterModel.items[0];
  switch (filterItem.operator) {
    case 'contains': {
      return { [filterItem.field]: stripQuotes(filterItem.value) };
    }
    case 'equals': {
      return { [filterItem.field]: `"${stripQuotes(filterItem.value)}"` };
    }
    // TODO: apply for filtering by User rating of flashcard. 
    // case '>=': {
    //   return { [`${filterItem.field}_min`]: filterItem.value };
    // }
    // case '<=':
    //   return { [`${filterItem.field}_max`]: filterItem.value };
    default:
      return { [filterItem.field]: filterItem.value };
  }
}

/**
 * Function to strip quotes from beginning and end of string value.
 * @param {string} value - String value to strip quotes from.
 * @return {string} - String value without quotes.
 */
function stripQuotes(value: string): string {
  if (value.startsWith('"')) {
    value = value.slice(1, value.length);
  }
  if (value.endsWith('"')) {
    value = value.slice(0, -1);
  }
  return value;
}
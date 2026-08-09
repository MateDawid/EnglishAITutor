import {
  getGridStringOperators,
  getGridNumericOperators,
  // getGridBooleanOperators,
  getGridSingleSelectOperators,
  type GridFilterModel,
} from '@mui/x-data-grid';

export const STRING_FILTER_OPERATORS = getGridStringOperators().filter((operator) =>
  ['contains'].includes(operator.value)
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
  console.log(updatedFilterModel);
  if (updatedFilterModel.items.length === 0) {
    return {};
  } else if (updatedFilterModel.items[0].value == null) {
    return {};
  }
  const filterItem = updatedFilterModel.items[0];
  switch (filterItem.operator) {
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

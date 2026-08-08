import type { GridSortModel } from "@mui/x-data-grid";

interface EmptySortModel {}

interface NonEmptySortModel { order_by: string }
  
export type ApiSortModel = EmptySortModel | NonEmptySortModel;

/**
 * Function for formatting sortModel for API calls purposes.
 * @param {GridSortModel} updatedSortModel - Updated sortModel returned from DataGrid after update.
 * @param {object} columns - Displayed columns settings.
 * @return {object} - Formatted sortModel for API calls.
 */
export function formatSortModel(updatedSortModel: GridSortModel): ApiSortModel {
  if (updatedSortModel.length === 0) {
    return {} as EmptySortModel;
  }
  const sortItem = updatedSortModel[0];
  const sortField = sortItem.field;
  return {
    order_by: sortItem.sort === 'desc' ? '-' + sortField : sortField,
  } as ApiSortModel;
}
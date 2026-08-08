export const PAGE_SIZE_OPTIONS = [10, 20, 50];

import type { GridPaginationModel } from '@mui/x-data-grid';

export interface ApiPaginationModel {
  /**
  * Set the number of rows in one page.
  */
  page_size: number;

  /**
 * The index of the current page.
 */
  page: number;
}

/**
 * Function for formatting pagination model for API calls purposes.
 * - Rename `pageSize` to `page_size`
 * - Increment `page` by 1
 *  
 * @param {GridPaginationModel} updatedPaginationModel - Updated pagination model returned from DataGrid after update.
 * @return {ApiPaginationModel} - Formatted pagination model for API calls.
 */
export function formatPaginationModel(updatedPaginationModel: GridPaginationModel): ApiPaginationModel {
  return {
    page: updatedPaginationModel.page + 1,
    page_size: updatedPaginationModel.pageSize,
  };
}

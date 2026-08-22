import Box from '@mui/material/Box';
import { styled } from '@mui/material/styles';
import { DataGrid } from '@mui/x-data-grid';

export const StyledBox = styled(Box)(() => ({
  flexGrow: 1,
  marginTop: 2,
  width: '100%',
  maxWidth: '100%',
  height: 600,
}));


export const StyledDataGrid = styled(DataGrid)(({ theme }) => ({
  margin: 8,
  border: `3px solid ${theme.palette.primary.dark} !important`,
  borderRadius: 0,
  boxShadow: `4px 4px 0 ${theme.palette.primary.dark} !important`,
  // Header and footer styling
  '& .MuiDataGrid-topContainer': {
    backgroundColor: `${theme.palette.primary.main} !important`,
    borderBottom: '0 !important',
  },
  '& .MuiDataGrid-columnHeader, .MuiDataGrid-footerContainer': {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.secondary.main,
  },
  '& .MuiDataGrid-filler, .MuiDataGrid-scrollbarFiller': {
    backgroundColor: `${theme.palette.primary.main} !important`,
  },
  '& .MuiSvgIcon-root': {
    color: `${theme.palette.primary.contrastText} !important`,
  },
  '& .MuiDataGrid-sortButton': {
    backgroundColor: `${theme.palette.primary.main} !important`,
  },
  '& .MuiDataGrid-columnHeaderTitle, .MuiTablePagination-selectLabel, .MuiTablePagination-select, .MuiTablePagination-displayedRows':
  {
    fontFamily: '"Arial Black", sans-serif !important',
    color: theme.palette.secondary.main,
  },
  '& .MuiDataGrid-columnSeparator': {
    display: 'none',
  },
  // Cells styling
  '& .MuiDataGrid-cell': {
    fontFamily: '"Arial", sans-serif !important',
  },
  '& .MuiDataGrid-row .MuiDataGrid-cell[data-field="word"]': {
    fontWeight: 'bold',
  },
}));

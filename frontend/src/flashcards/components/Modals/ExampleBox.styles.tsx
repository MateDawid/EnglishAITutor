import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledExampleBox = styled(Box)(({ theme }) => ({
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    boxSizing: 'border-box',
    backgroundColor: theme.palette.primary.light,
    padding: 0,
    border: `3px solid ${theme.palette.primary.dark}`,
    minWidth: 0,
    overflowWrap: 'anywhere',
}));

export const ExampleTitleBox = styled(Box)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    padding: "4px",
    margin: 0,
    borderRight: `3px solid ${theme.palette.primary.dark}`,
    borderBottom: `3px solid ${theme.palette.primary.dark}`,
}));

export const ExampleTitleTypography = styled(Typography)(({ theme }) => ({
    fontFamily: '"Arial", sans-serif !important',
    fontWeight: 'bold !important',
    fontSize: '10px',
    fontColor: theme.palette.primary.contrastText,
}));

export const ExampleTypography = styled(Typography)(({ theme }) => ({
    fontFamily: '"Arial", sans-serif !important',
    textAlign: 'justify',
    color: theme.palette.primary.contrastText,
    margin: 8,
    padding: 8,
    paddingTop: 0,
}));
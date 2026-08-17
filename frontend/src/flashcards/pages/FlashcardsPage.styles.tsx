import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';

export const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: 16,
  margin: 16,
  border: `3px solid ${theme.palette.primary.dark}`,
  borderRadius: 0,
  boxShadow: `3px 3px 0 ${theme.palette.primary.dark}`,
  height: '100%',
}));

export const StyledTypography = styled(Typography)(({ theme }) => ({
  fontFamily: '"Arial Black", sans-serif !important',
  fontWeight: 'normal !important',
  color: theme.palette.primary.main,
}));

export const StyledDivider = styled(Divider)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.primary.dark,
  height: '3px',
}));
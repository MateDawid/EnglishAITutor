import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

export const StyledPaper = styled(Paper)(() => ({
  padding: 16,
  margin: 16,
  border: '3px solid #1f1f1f',
  borderRadius: 0,
  boxShadow: '3px 3px 0 #1f1f1f',
  height: '100%',
}));


export const StyledTypography = styled(Typography)(() => ({
  fontFamily: '"Arial Black", sans-serif !important',
  fontWeight: 'normal !important',
}));
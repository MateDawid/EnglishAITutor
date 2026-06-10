import { AppBar, Toolbar, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledAppBar = styled(AppBar)({
  backgroundColor: '#BD0000',
});

export const StyledToolbar = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'space-between',
});

export const StyledTypography = styled(Typography)<{ component?: React.ElementType; href?: string }>({
  textDecoration: 'none',
  fontFamily: 'monospace',
  fontWeight: 700,
  letterSpacing: '.3rem',
  color: 'inherit',
});

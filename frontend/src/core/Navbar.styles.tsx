import { AppBar, Toolbar, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import School from '@mui/icons-material/School';


export const StyledAppBar = styled(AppBar)({
  backgroundColor: 'primary',
});

export const StyledToolbar = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'flex-start',
  gap: '2rem',
});

export const StyledTypography = styled(Typography)<{ component?: React.ElementType; href?: string }>({
  textDecoration: 'none',
  fontFamily: 'system-ui',
  color: 'inherit',
});

export const StyledIconButton = styled(IconButton)<{ component?: React.ElementType; href?: string }>({
  color: '#ffffff',
});

export const StyledSchoolIcon = styled(School)({
  fontSize: 40,
});

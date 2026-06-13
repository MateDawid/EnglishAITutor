import { AppBar, Button, Toolbar, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import School from '@mui/icons-material/School';


export const StyledAppBar = styled(AppBar)({
  backgroundColor: 'primary',
});

export const StyledToolbar = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'space-between'
});

export const StyledTypography = styled(Typography)<{ component?: React.ElementType; href?: string }>(({ theme }) => ({
  textDecoration: 'none',
  fontFamily: 'system-ui',
  color: 'inherit',
  display: 'none',
  [theme.breakpoints.up('sm')]: {
    display: 'block'
  }
}));

export const StyledIconButton = styled(IconButton)<{ component?: React.ElementType; href?: string }>({
  color: '#ffffff',
});

export const StyledSchoolIcon = styled(School)({
  fontSize: 40,
});

export const StyledButton = styled(Button)(({ theme }) => ({
  color: '#ffffff',
  display: 'none',
  [theme.breakpoints.up('sm')]: {
    display: 'flex'
  }
}));
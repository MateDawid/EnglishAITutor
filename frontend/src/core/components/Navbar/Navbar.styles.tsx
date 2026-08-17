import { AppBar, Button, Toolbar, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import IconButton from '@mui/material/IconButton';
import School from '@mui/icons-material/School';


export const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  borderBottom: `2px solid ${theme.palette.primary.contrastText}`,
}));

export const StyledToolbar = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'space-between',
});

export const StyledTypography = styled(Typography)<{ component?: React.ElementType; href?: string }>(({ theme }) => ({
  textDecoration: 'none',
  fontFamily: '"Arial Black", sans-serif !important',
  fontWeight: 'normal !important',
  fontSize: '14px !important',
  color: 'inherit',
  display: 'none',
  [theme.breakpoints.up('sm')]: {
    display: 'block'
  }
}));

export const StyledIconButton = styled(IconButton)<{ component?: React.ElementType; href?: string }>(({ theme }) => ({
  color: theme.palette.primary.contrastText,
  '&:hover': {
    boxShadow: 'none',
  },
}));

export const StyledSchoolIcon = styled(School)({
  fontSize: 40,

});


export const StyledButton = styled(Button)(({ theme }) => ({
  display: 'none',
  color: theme.palette.primary.contrastText,
  borderRadius: 0,
  border: `0px`,
  boxShadow: 'none',
  fontFamily: '"Arial Black", sans-serif !important',
  fontWeight: 'normal !important',
  fontSize: '14px !important',
  '&:hover': {
    boxShadow: 'none',
  },
  [theme.breakpoints.up('sm')]: {
    display: 'flex'
  }
}));
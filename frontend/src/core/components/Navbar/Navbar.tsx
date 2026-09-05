import Stack from '@mui/material/Stack';
import { StyledButton, StyledAppBar, StyledIconButton, StyledSchoolIcon, StyledToolbar } from './Navbar.styles';
import NavbarMenu from './NavbarMenu';
import { Logout } from '@mui/icons-material';
import navConfig from './navConfig';
import { removeAccessTokenFromLocalStorage } from '../../../auth/services/LoginService';
import { useNavigate } from 'react-router-dom';

/**
 * Navbar component to display navigation bar on top of the page.
 */
export const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeAccessTokenFromLocalStorage();
    navigate('/login');
  }

  return (
    <StyledAppBar position="sticky">
      <StyledToolbar>
        <Stack direction="row" spacing={5} sx={{ justifyContent: 'space-between', alignItems: 'center' }}>
          <StyledIconButton
            component="a"
            href="/"
          >
            <StyledSchoolIcon />
          </StyledIconButton>
          {navConfig.map((item) => (
            <StyledButton
              key={item.url}
              variant="outlined"
              onClick={() => navigate(item.url)}
              startIcon={item.icon}
            >
              {item.label}
            </StyledButton>
          ))}
        </Stack>
        <StyledButton
          variant="outlined"
          onClick={handleLogout}
          startIcon={<Logout />}
        >
          Logout
        </StyledButton>
        <NavbarMenu sx={{ display: { xs: 'block', sm: 'none' } }} />
      </StyledToolbar>
    </StyledAppBar>
  );
};

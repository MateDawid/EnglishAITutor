import Stack from '@mui/material/Stack';
import { StyledButton, StyledAppBar, StyledIconButton, StyledSchoolIcon, StyledToolbar, StyledTypography } from './Navbar.styles';
import NavbarMenu from './NavbarMenu';
import { Logout } from '@mui/icons-material';
import navConfig from './navConfig';

/**
 * Navbar component to display navigation bar on top of the page.
 */
export const Navbar = () => {
  return (
    <StyledAppBar position="sticky">
      <StyledToolbar>
        <Stack direction="row" spacing={4} sx={{ justifyContent: 'space-between', alignItems: 'center' }}>
          <StyledIconButton
            component="a"
            href="/"
          >
            <StyledSchoolIcon />
          </StyledIconButton>
          {navConfig.map((item) => (
            <StyledTypography
              variant="subtitle1"
              component="a"
              href={item.url}
              key={item.url}
            >
              {item.label}
            </StyledTypography>
          ))}
        </Stack>
        <StyledButton
          variant="outlined"
          onClick={() => { }}
          startIcon={<Logout />}
        >
          Logout
        </StyledButton>
        <NavbarMenu sx={{ display: { xs: 'block', sm: 'none' } }} />
      </StyledToolbar>
    </StyledAppBar>
  );
};

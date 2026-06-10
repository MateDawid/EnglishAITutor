import { StyledAppBar, StyledToolbar, StyledTypography } from './Navbar.styles';

/**
 * Navbar component to display navigation bar on top of the page.
 */
const Navbar = () => {
  return (
    <StyledAppBar position="sticky">
      <StyledToolbar>
        <StyledTypography
          variant="h6"
          component="a"
          href="/"
        >
          ENGLISH AI TUTOR
        </StyledTypography>
      </StyledToolbar>
    </StyledAppBar>
  );
};

export default Navbar;
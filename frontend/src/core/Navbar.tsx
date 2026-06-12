import { StyledAppBar, StyledIconButton, StyledSchoolIcon, StyledToolbar, StyledTypography } from './Navbar.styles';

/**
 * Navbar component to display navigation bar on top of the page.
 */
const Navbar = () => {
  return (
    <StyledAppBar position="sticky">
      <StyledToolbar>
        <StyledIconButton 
          component="a" 
          href="/"
        >
          <StyledSchoolIcon/>
        </StyledIconButton>
        <StyledTypography
          variant="subtitle1"
          component="a"
          href="/flashcards"
        >
          Flashcards
        </StyledTypography>
        <StyledTypography
          variant="subtitle1"
          component="a"
          href="/chat"
        >
          Chat with Tutor
        </StyledTypography>
      </StyledToolbar>
    </StyledAppBar>
  );
};

export default Navbar;
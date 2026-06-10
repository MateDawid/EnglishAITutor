import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Navbar from './Navbar.tsx';
import Leftbar from './Leftbar.tsx';
import { StyledStack, StyledMainBox } from './BasePage.styles';

export default function BasePage() {

  return (
    <Box>
      <Navbar />
      <StyledStack direction="row">
        <Leftbar />
        <StyledMainBox component="main">
          <Outlet />
        </StyledMainBox>
      </StyledStack>
    </Box>
  );
}
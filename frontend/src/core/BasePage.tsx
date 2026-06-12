import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Navbar from './Navbar.tsx';
import { StyledMainBox } from './BasePage.styles';

export default function BasePage() {

  return (
    <Box>
      <Navbar />
      <StyledMainBox component="main">
        <Outlet />
      </StyledMainBox>
    </Box>
  );
}
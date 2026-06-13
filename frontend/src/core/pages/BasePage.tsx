import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import { StyledMainBox } from './BasePage.styles';
import { Navbar } from '../components/Navbar';

export function BasePage() {

  return (
    <Box>
      <Navbar />
      <StyledMainBox component="main">
        <Outlet />
      </StyledMainBox>
    </Box>
  );
}
// src/components/NavbarMenu.tsx
import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Box, Divider } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Logout } from '@mui/icons-material';
import navConfig from './navConfig';


/**
 * NavbarMenu component to display Navbar menu on small screens.
 */
export default function NavbarMenu({ ...props }) {
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => setAnchorEl(null);

  const handleLogout = () => {
    console.log('Logout clicked');
  };

  return (
    <Box {...props}>
      <IconButton color="inherit" onClick={handleClick}>
        <MenuIcon />
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
      >
        {navConfig.map((item) => (
          <MenuItem
            key={item.url}
            component={RouterLink}
            to={item.url}
            onClick={handleClose}
            sx={{ gap: 1 }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText>{item.label}</ListItemText>
          </MenuItem>
        ))}
        <Divider/>
        <MenuItem onClick={handleLogout} sx={{ gap: 1 }}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          <ListItemText>Logout</ListItemText>
        </MenuItem>
      </Menu>
    </Box>
  );
}
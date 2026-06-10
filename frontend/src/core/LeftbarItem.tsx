import { Link } from '@mui/material';
import * as React from 'react';
import { StyledListItemButton, StyledListItemIcon, StyledListItemText, iconStyle } from './LeftbarItem.styles';

/**
 * LeftbarItem component to display single navigation item in Leftbar.
 */
const LeftbarItem = ({ url, displayText, icon }: { url: string; displayText: string; icon: React.ReactElement }) => {
  return (
    <StyledListItemButton component={Link} to={url}>
      <StyledListItemIcon>
        {React.cloneElement(icon, { style: iconStyle } as any)}
      </StyledListItemIcon>
      <StyledListItemText primary={displayText} />
    </StyledListItemButton>
  );
};

export default LeftbarItem;
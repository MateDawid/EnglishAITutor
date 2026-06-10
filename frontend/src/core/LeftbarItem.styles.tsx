import { ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledListItemButton = styled(ListItemButton)<{ component?: React.ElementType; to?: string }>({
  justifyContent: 'center',
  minHeight: 48,
});

export const StyledListItemIcon = styled(ListItemIcon)({
  justifyContent: 'center',
  minWidth: 0,
  marginRight: 15,
});

export const StyledListItemText = styled(ListItemText)({
  color: '#FFFFFF',
});

export const iconStyle = {
  color: '#BD0000',
};

import { Box, Stack } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledStack = styled(Stack)({
  minHeight: '100vh',
});

export const StyledMainBox = styled(Box)<{ component?: React.ElementType }>({
  justifyContent: 'center',
  alignItems: 'center',
});

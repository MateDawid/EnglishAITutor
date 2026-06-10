import { Box, Stack } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledStack = styled(Stack)({
  minHeight: '100vh',
});

export const StyledMainBox = styled(Box)<{ component?: React.ElementType }>({
  flex: 1,
  minWidth: 0,
  paddingTop: 2,
  paddingLeft: 2,
  paddingRight: 2,
});

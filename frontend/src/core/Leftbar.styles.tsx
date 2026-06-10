import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

export const OuterBox = styled(Box)({
  width: 180,
  height: '100%',
  zIndex: 999,
  backgroundColor: '#252525',
});

export const InnerBox = styled(Box)({
  position: 'fixed',
  height: '100%',
  width: 180,
  backgroundColor: '#252525',
  overflow: 'auto',
});

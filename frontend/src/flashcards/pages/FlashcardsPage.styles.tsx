import { styled } from '@mui/material/styles';
import { StyledPaper } from '../../styles';

export const FlashcardsPaper = styled(StyledPaper)(({ theme }) => ({
  // padding: 16,
  // margin: '16px auto',
  // border: `3px solid ${theme.palette.primary.dark}`,
  // borderRadius: 0,
  // boxShadow: `3px 3px 0 ${theme.palette.primary.dark}`,
  [theme.breakpoints.up('xs')]: {
    width: '80%',
  },
  [theme.breakpoints.up('sm')]: {
    width: '60%',
  },
  [theme.breakpoints.up('md')]: {
    width: '50%',
  },
}));

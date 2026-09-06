import { Box, Button } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledRatingBox = styled(Box)({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    margin: 0,
    alignItems: 'center',
});

export const ButtonsBox = styled(Box)({
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    margin: 0
});

const BaseButton = styled(Button)(({ theme }) => ({
    width: '100%',
    borderRadius: 0,
    borderTop: `3px solid ${theme.palette.primary.dark}`,
}));

export const EasyButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: theme.palette.primary.ratingEasyLight,
    '&:hover': {
        backgroundColor: theme.palette.primary.ratingEasyDark,
    },
    borderRight: `3px solid ${theme.palette.primary.dark}`,
}));

export const MediumButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: theme.palette.primary.ratingMediumLight,
    '&:hover': {
        backgroundColor: theme.palette.primary.ratingMediumDark,
    },
}));

export const HardButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: theme.palette.primary.ratingHardLight,
    borderLeft: `3px solid ${theme.palette.primary.dark}`,
    '&:hover': {
        backgroundColor: theme.palette.primary.ratingHardDark,
    },
}));
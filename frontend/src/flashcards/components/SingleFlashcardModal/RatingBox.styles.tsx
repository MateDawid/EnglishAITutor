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
    backgroundColor: '#2E7D32',
    '&:hover': {
        backgroundColor: '#1B5E20',
    },
    borderRight: `3px solid ${theme.palette.primary.dark}`,
}));

export const MediumButton = styled(BaseButton)({
    color: 'white',
    backgroundColor: '#F57C00',
    '&:hover': {
        backgroundColor: '#EF6C00',
    },
});

export const HardButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: '#C62828',
    borderLeft: `3px solid ${theme.palette.primary.dark}`,
    '&:hover': {
        backgroundColor: '#B71C1C',
    },
}));
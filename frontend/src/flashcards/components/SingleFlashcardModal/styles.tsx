import { Modal, Box, Typography, Paper, Button, Chip } from '@mui/material';
import { styled } from '@mui/material/styles';

// MODAL

export const StyledModal = styled(Modal)({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    perspective: '1200px',
});

// TYPOGRAPHY

const BaseTypography = styled(Typography)(({ theme }) => ({
    fontFamily: '"Arial Black", sans-serif !important',
    fontWeight: 'normal !important',
    color: theme.palette.primary.main,
    alignSelf: 'center',
}));

export const HeaderTypography = styled(BaseTypography)({});

export const WordTypography = styled(BaseTypography)({
    margin: 0, 
    padding: 0
});

export const MeaningTypography = styled(BaseTypography)({
    fontFamily: '"Arial", sans-serif !important',
    width: '100%',
    textAlign: 'justify',
    textJustify: 'inter-word',

});

export const ExampleTypography = styled(BaseTypography)({
    fontFamily: '"Arial", sans-serif !important',
    width: '100%',
    textAlign: 'justify',
    textJustify: 'inter-word',
});

// CARD

export const StyledPaper = styled(Paper, {
    shouldForwardProp: (prop) => prop !== 'reversed',
})<{ reversed: boolean }>(({ theme, reversed }) => ({
    position: 'relative',
    marginTop: 24,
    padding: 24,
    width: 420,
    maxWidth: '90vw',
    minHeight: 350,
    border: `3px solid ${theme.palette.primary.dark}`,
    borderRadius: 0,
    transformStyle: 'preserve-3d',
    transition: 'transform 0.6s ease',
    transform: reversed ? 'rotateY(180deg)' : 'rotateY(0deg)',
}));

export const PaperFace = styled(Box)(() => ({
    position: 'absolute',
    width: '100%',
    height: '100%',
    top: 0,
    left: 0,

    padding: 0,
    paddingTop: 16,
    boxSizing: 'border-box',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-start',
    backfaceVisibility: 'hidden',
    WebkitBackfaceVisibility: 'hidden',
}));


export const PaperBack = styled(PaperFace)({
    transform: 'rotateY(180deg)',
    overflowY: 'auto',
    overflowX: 'hidden',
    justifyContent: 'flex-start',
    alignItems: 'stretch',
    height: '100%',
});

export const CardBox = styled(Box)({
    height: '100%',
    width: '100%',
    padding: 0,
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    alignItems: 'center',
});

// BUTTON

const BaseButton = styled(Button)(({ theme }) => ({
    width: '100%',
    borderRadius: 0,
    borderTop: `3px solid ${theme.palette.primary.dark}`,
}));

export const RevealButton = styled(BaseButton)({});

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

// BOXES

export const WordBox = styled(Box)({
    display: 'flex', flexDirection: 'row', alignItems: 'center', gap: 8
});

export const MeaningBox = styled(Box)({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    padding: 16,
    gap: 8,
});

export const ButtonsBox = styled(Box)({
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    margin: 0
});

// CHIP

export const StyledChip = styled(Chip)(() => ({
    fontFamily: '"Arial", sans-serif !important',
    fontWeight: 'bold !important',
    margin: 0,
    padding: 0,
}));
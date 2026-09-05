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
    margin: 0,
    padding: 0,
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


export const RevealButton = styled(Button)(({ theme }) => ({
    width: '100%',
    borderRadius: 0,
    borderTop: `3px solid ${theme.palette.primary.dark}`,
}));

export const EasyChip = styled(Chip)({
    color: 'white',
    backgroundColor: '#2E7D32',
});



export const MediumChip = styled(Chip)({
    color: 'white',
    backgroundColor: '#F57C00',
});




export const HardChip = styled(Chip)({
    color: 'white',
    backgroundColor: '#C62828',
});
// BOXES

export const WordBox = styled(Box)({
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8
});

export const MeaningBox = styled(Box)({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    width: '80%',
    padding: 16,
    gap: 24,
});


// CHIP

export const StyledChip = styled(Chip)(({ theme }) => ({
    fontFamily: '"Arial", sans-serif !important',
    fontWeight: 'bold !important',
    margin: 0,
    padding: 0,
    marginRight: 4,
    color: theme.palette.primary.contrastText,
    backgroundColor: theme.palette.primary.main,
}));
import { Box, Typography, Paper, Button, Chip } from '@mui/material';
import { useEffect, useState } from 'react';
import { styled } from '@mui/material/styles';
import { Modal } from '@mui/material';

// MODAL

const StyledModal = styled(Modal)({
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

export const WordTypography = styled(BaseTypography)({});

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

const StyledPaper = styled(Paper, {
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

const PaperFace = styled(Box)(() => ({
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

const PaperBack = styled(PaperFace)({
    transform: 'rotateY(180deg)',
    overflowY: 'auto',
    overflowX: 'hidden',
    justifyContent: 'flex-start',
    alignItems: 'stretch',
    height: '100%',
});

const CardBox = styled(Box)({
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

const RevealButton = styled(BaseButton)({});

const EasyButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: '#2E7D32',
    '&:hover': {
        backgroundColor: '#1B5E20',
    },
    borderRight: `3px solid ${theme.palette.primary.dark}`,
}));

const MediumButton = styled(BaseButton)({
    color: 'white',
    backgroundColor: '#F57C00',
    '&:hover': {
        backgroundColor: '#EF6C00',
    },
});

const HardButton = styled(BaseButton)(({ theme }) => ({
    color: 'white',
    backgroundColor: '#C62828',
    borderLeft: `3px solid ${theme.palette.primary.dark}`,
    '&:hover': {
        backgroundColor: '#B71C1C',
    },
}));

// BOXES

// display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1, padding: 2,
const MeaningBox = styled(Box)({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: 16,
    gap: 1
});

const ButtonsBox = styled(Box)({
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    margin: 0
});

// TYPING

type Flashcard = {
    word: string;
    meaning: string;
    part_of_speech: string;
    example: string | null;
};


type SingleFlashcardModalProps = {
    flashcard: Flashcard;
    open: boolean;
    setOpen: (open: boolean) => void;
};

/**
 * FormModal component for displaying add/edit form.
 * @param {object} props
 * @param {object} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {boolean} props.open - Flag indicating if form is opened.
 * @param {function} props.setOpen - Setter for open flag.
 */
const SingleFlashcardModal = ({
    flashcard,
    open,
    setOpen,
}: SingleFlashcardModalProps) => {
    const [cardReversed, setCardReversed] = useState(false);

    useEffect(() => {
        if (!open) {
            setCardReversed(false);
        }
    }, [open]);

    return (
        <StyledModal
            open={open}
            onClose={() => {
                setOpen(false);
                setCardReversed(false);
            }}
        >
            <StyledPaper reversed={cardReversed}>
                <PaperFace>
                    <CardBox>
                        <HeaderTypography variant="h6" gutterBottom>
                            Word
                        </HeaderTypography>
                        <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: 1 }}>
                            <WordTypography variant="h4" gutterBottom sx={{ margin: 0, padding: 0 }}>
                                {flashcard.word}
                            </WordTypography>
                            <Chip variant="outlined" color="primary" size="small" label={flashcard.part_of_speech} sx={{ margin: 0, padding: 0 }} />
                        </Box>
                        <RevealButton
                            variant="contained"
                            onClick={() => setCardReversed(true)}
                        >
                            Reveal
                        </RevealButton>
                    </CardBox>
                </PaperFace>
                <PaperBack>
                    <CardBox>
                        <HeaderTypography variant="h6" gutterBottom>
                            Meaning
                        </HeaderTypography>
                        <MeaningBox>
                            <MeaningTypography variant="body1" gutterBottom sx={{ margin: 0, padding: 0 }}>
                                {flashcard.meaning}
                            </MeaningTypography>
                            {flashcard.example && (
                                <>
                                    <Chip variant="filled" color="primary" size="small" label="Example" sx={{ margin: 0, padding: 0 }} />
                                    <ExampleTypography variant="body2" gutterBottom>
                                        {flashcard.example}
                                    </ExampleTypography>
                                </>

                            )}
                        </MeaningBox>
                        <ButtonsBox>
                            <EasyButton
                                variant="contained"
                                onClick={() => setOpen(false)}
                            >
                                Easy
                            </EasyButton>
                            <MediumButton
                                variant="contained"
                                onClick={() => setOpen(false)}
                            >
                                Medium
                            </MediumButton>
                            <HardButton
                                variant="contained"
                                onClick={() => setOpen(false)}
                            >
                                Hard
                            </HardButton>
                        </ButtonsBox>
                    </CardBox>
                </PaperBack>
            </StyledPaper>
        </StyledModal>
    );
};

export default SingleFlashcardModal;

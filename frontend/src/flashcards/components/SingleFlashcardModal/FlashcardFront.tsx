
import { Box, Chip } from '@mui/material';
import { PaperFace, CardBox, HeaderTypography, WordTypography, RevealButton, StyledChip } from './styles';
import type { Flashcard } from '../../types';
import type { JSX } from '@emotion/react/jsx-dev-runtime';


/**
 * Component for displaying the front of a flashcard, containing its word and part of speech.
 * 
 * @param {Flashcard} flashcard - The flashcard data to be displayed on the front of the flashcard.
 * @param {function} setCardReversed - Setter for card reversed flag.
 * @returns {JSX.Element} The JSX element for the front of the flashcard.
 */
const FlashcardFront = ({ flashcard, setCardReversed }: { flashcard: Flashcard, setCardReversed: (reversed: boolean) => void }): JSX.Element => {
    return (
        <PaperFace>
            <CardBox>
                <HeaderTypography variant="h6" gutterBottom>
                    Word
                </HeaderTypography>
                <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', gap: 1 }}>
                    <WordTypography variant="h4" gutterBottom sx={{ margin: 0, padding: 0 }}>
                        {flashcard.word}
                    </WordTypography>
                    <StyledChip variant="outlined" color="primary" size="small" label={flashcard.part_of_speech} />
                </Box>
                <RevealButton
                    variant="contained"
                    onClick={() => setCardReversed(true)}
                >
                    Reveal
                </RevealButton>
            </CardBox>
        </PaperFace>
    );
};

export default FlashcardFront;
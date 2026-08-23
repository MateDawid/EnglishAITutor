
import { Box, Chip } from '@mui/material';
import { PaperFace, CardBox, HeaderTypography, WordTypography, RevealButton } from './styles';
import type { Flashcard } from './types';


/**
 * Component for displaying the front of a flashcard, containing its word and part of speech.
 * 
 * @param flashcard - The flashcard data to be displayed on the front of the flashcard.
 * @param setCardReversed - Setter for card reversed flag.
 * @returns The JSX element for the front of the flashcard.
 */
const FlashcardFront = ({ flashcard, setCardReversed }: { flashcard: Flashcard, setCardReversed: (reversed: boolean) => void }) => {
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
    );
};

export default FlashcardFront;
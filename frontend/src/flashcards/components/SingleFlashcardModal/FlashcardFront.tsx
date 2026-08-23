
import { PaperFace, CardBox, HeaderTypography, WordTypography, RevealButton, StyledChip, WordBox } from './styles';
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
                <WordBox>
                    <WordTypography variant="h4" gutterBottom>
                        {flashcard.word}
                    </WordTypography>
                    <StyledChip variant="outlined" color="primary" size="small" label={flashcard.part_of_speech} />
                </WordBox>
                <RevealButton variant="contained" onClick={() => setCardReversed(true)}>
                    Reveal
                </RevealButton>
            </CardBox>
        </PaperFace>
    );
};

export default FlashcardFront;
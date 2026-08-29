import { PaperBack, CardBox, HeaderTypography, MeaningBox, MeaningTypography, StyledChip, WordBox } from "./styles";
import type { Flashcard } from "../../types";
import type { JSX } from "@emotion/react/jsx-dev-runtime";
import ExampleBox from "./ExampleBox";
import RatingBox from "./RatingBox";

type FlashcardBackProps = {
    flashcard: Flashcard;
    handleClose: () => void;
};

/**
 * Component for displaying the back of a flashcard, containing its meaning, example, and difficulty buttons.
 * 
 * @param {Flashcard} flashcard - The flashcard data to be displayed on the back of the flashcard.
 * @param {function} handleClose - Function to handle closing the flashcard back.
 * @returns {JSX.Element} The JSX element for the back of the flashcard.
 */
const FlashcardBack = ({ flashcard, handleClose }: FlashcardBackProps): JSX.Element => {
    return (
        <PaperBack>
            <CardBox>
                <WordBox>
                    <HeaderTypography variant="body2" gutterBottom>
                        {flashcard.word} <StyledChip variant="outlined" color="primary" size="small" label={flashcard.part_of_speech} />
                    </HeaderTypography>
                </WordBox>
                <MeaningBox>
                    <MeaningTypography variant="body1" gutterBottom>
                        {flashcard.meaning}
                    </MeaningTypography>
                    {flashcard.example && (
                        <ExampleBox example={flashcard.example} />
                    )}
                </MeaningBox>
                <RatingBox handleClose={handleClose} />
            </CardBox>
        </PaperBack>
    )
}

export default FlashcardBack;
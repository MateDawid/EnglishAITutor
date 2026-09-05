import { PaperBack, CardBox, HeaderTypography, MeaningBox, MeaningTypography, StyledChip, WordBox } from "./styles";
import type { Flashcard } from "../../types";
import type { JSX } from "@emotion/react/jsx-dev-runtime";
import type { FlashcardRating } from "../../../flashcards/constants";
import ExampleBox from "./ExampleBox";
import RatingBox from "./RatingBox";
import apiClient from "../../../core/apiClient";

type FlashcardBackProps = {
    flashcard: Flashcard;
    handleClose: () => void;
    setRefreshTimestamp: (timestamp: number | null) => void;
};

/**
 * Component for displaying the back of a flashcard, containing its meaning, example, and difficulty buttons.
 * 
 * @param {Flashcard} flashcard - The flashcard data to be displayed on the back of the flashcard.
 * @param {function} handleClose - Function to handle closing the flashcard back.
 * @returns {JSX.Element} The JSX element for the back of the flashcard.
 */
const FlashcardBack = ({ flashcard, handleClose, setRefreshTimestamp }: FlashcardBackProps): JSX.Element => {
    /**
     * Handles rating the flashcard with the given difficulty.
     *
     * @param rating - The difficulty rating to be applied to the flashcard.
     */
    const handleRate = async (rating: FlashcardRating) => {
        try {
            const response = await apiClient.post(`/flashcards/${flashcard.id}/`, { rating: rating });
            if (response.status === 201 && response.data.rating_changed) {
                setRefreshTimestamp(Date.now());
            }
        } 
        catch (error) {
            console.error('Error rating the flashcard:', error);
        }
        finally {
            handleClose();
        }
    };
    
    return (
        <PaperBack>
            <CardBox>
                <WordBox>
                    <HeaderTypography variant="body2" gutterBottom>
                        {flashcard.word}
                    </HeaderTypography>
                    <StyledChip variant="outlined" color="primary" size="small" label={flashcard.part_of_speech} />
                </WordBox>
                <MeaningBox>
                    <MeaningTypography variant="body1" gutterBottom>
                        {flashcard.meaning}
                    </MeaningTypography>
                    {flashcard.example && (
                        <ExampleBox example={flashcard.example} />
                    )}
                </MeaningBox>
                <RatingBox handleClose={handleClose} handleRate={handleRate} />
            </CardBox>
        </PaperBack>
    )
}

export default FlashcardBack;
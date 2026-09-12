import type { JSX } from "@emotion/react/jsx-dev-runtime";
import { Typography } from "@mui/material";
import { StyledRatingBox, ButtonsBox, EasyButton, MediumButton, HardButton } from "./RatingBox.styles";
import { FlashcardRating } from "../../constants";

type RatingBoxProps = {
    handleRate: (rating: FlashcardRating) => void;
};

/**
 * Component that displays the rating box with tooltip on Flashcard back.
 * 
 * @param {function} handleRate - Function to handle rating the flashcard with the given difficulty.
 * @returns {JSX.Element} A JSX element representing the rating box.
 */
const RatingBox = ({ handleRate }: RatingBoxProps): JSX.Element => {
    return (
        <StyledRatingBox>
            <Typography variant="body2" gutterBottom>
                How hard was this word for you?
            </Typography>
            <ButtonsBox>
                <EasyButton variant="contained" onClick={async () => await handleRate(FlashcardRating.EASY)}>
                    Easy
                </EasyButton>
                <MediumButton variant="contained" onClick={async () => await handleRate(FlashcardRating.MEDIUM)}>
                    Medium
                </MediumButton>
                <HardButton variant="contained" onClick={async () => await handleRate(FlashcardRating.HARD)}>
                    Hard
                </HardButton>
            </ButtonsBox>
        </StyledRatingBox>
    );
};

export default RatingBox;
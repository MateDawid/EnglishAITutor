import type { JSX } from "@emotion/react/jsx-dev-runtime";
import { Typography } from "@mui/material";
import { StyledRatingBox, ButtonsBox, EasyButton, MediumButton, HardButton } from "./RatingBox.styles";
import { EASY_RATING_VALUE, MEDIUM_RATING_VALUE, HARD_RATING_VALUE } from "../../constants";

type RatingBoxProps = {
    setOpen: (open: boolean) => void;
};

/**
 * Component that displays the rating box with tooltip on Flashcard back.
 * 
 * @param {function} setOpen - Setter for open flag.
 * @returns {JSX.Element} A JSX element representing the rating box.
 */
const RatingBox = ({ setOpen }: RatingBoxProps): JSX.Element => {

    const onButtonClick = (difficulty: number) => {
        // TODO: Perform API call for rating the flashcard with the selected difficulty value
        console.log(`User rated the word as: ${difficulty}`);
        setOpen(false);
    }

    return (
    <StyledRatingBox>
        <Typography variant="body2" gutterBottom>
            How hard was this word for you?
        </Typography>
        <ButtonsBox>
            <EasyButton variant="contained" onClick={() => onButtonClick(EASY_RATING_VALUE)}>
                Easy
            </EasyButton>
            <MediumButton variant="contained" onClick={() => onButtonClick(MEDIUM_RATING_VALUE)}>
                Medium
            </MediumButton>
            <HardButton variant="contained" onClick={() => onButtonClick(HARD_RATING_VALUE)}>
                Hard
            </HardButton>
        </ButtonsBox>
    </StyledRatingBox>
    );
};

export default RatingBox;
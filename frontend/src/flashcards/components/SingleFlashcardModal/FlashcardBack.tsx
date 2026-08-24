import { PaperBack, CardBox, HeaderTypography, MeaningBox, MeaningTypography, ExampleTypography, ButtonsBox, EasyButton, MediumButton, HardButton, StyledChip, ExampleBox } from "./styles";
import type { Flashcard } from "../../types";
import type { JSX } from "@emotion/react/jsx-dev-runtime";

type FlashcardBackProps = {
    flashcard: Flashcard;
    setOpen: (open: boolean) => void;
};

/**
 * Component for displaying the back of a flashcard, containing its meaning, example, and difficulty buttons.
 * 
 * @param {Flashcard} flashcard - The flashcard data to be displayed on the back of the flashcard.
 * @param {function} setOpen - Setter for open flag.
 * @returns {JSX.Element} The JSX element for the back of the flashcard.
 */
const FlashcardBack = ({ flashcard, setOpen }: FlashcardBackProps): JSX.Element => {
    return (
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
                        <ExampleBox>
                            <ExampleTypography variant="body2" gutterBottom>
                                <StyledChip variant="filled" color="primary" size="small" label="Example" />
                                {flashcard.example}
                            </ExampleTypography>
                        </ExampleBox>
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
    )
}

export default FlashcardBack;
import { Chip } from "@mui/material";
import { PaperBack, CardBox, HeaderTypography, MeaningBox, MeaningTypography, ExampleTypography, ButtonsBox, EasyButton, MediumButton, HardButton } from "./styles";
import type { Flashcard } from "./types";

const FlashcardBack = ({ flashcard, setOpen }: { flashcard: Flashcard, setOpen: (open: boolean) => void }) => {
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
    )
}

export default FlashcardBack;
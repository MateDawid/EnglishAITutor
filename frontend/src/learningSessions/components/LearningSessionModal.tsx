import { useState, useEffect } from "react";
import type { JSX } from "react";
import apiClient from "../../core/apiClient";
import { useAlertContext } from "../../core/store/AlertContext";
import FlashcardPaper from "../../flashcards/components/SingleFlashcardModal/FlashcardPaper";
import type { Flashcard } from "../../flashcards/types";
import { StyledModal } from "../../flashcards/components/SingleFlashcardModal/styles";
import { Box } from "@mui/material";
import { StyledPagination, StyledPaginationItem } from "./LearningSessionModal.styles";



type LearningSessionModalProps = {
    open: boolean;
    setOpen: (open: boolean) => void;
};

/**
 * LearningSessionModal component for displaying a learning session modal.
 * @param {object} props
 * @param {Flashcard} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {boolean} props.open - Flag indicating if modal is opened.
 * @param {function} props.setOpen - Setter for open flag.
 * @param {function} props.setRefreshTimestamp - Setter for refresh timestamp.
 */
const LearningSessionModal = ({
    open,
    setOpen,
}: LearningSessionModalProps): JSX.Element => {
    const { setAlert } = useAlertContext();
    const [cardReversed, setCardReversed] = useState(false);
    const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
    const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0);

    /**
     * Fetches objects list from API.
     */
    useEffect(() => {
        const loadData = async () => {
            try {
                const response = await apiClient.get('/flashcards/?page=1&page_size=10');
                setFlashcards(response.data.items);
            } catch {
                setAlert({
                    type: 'error',
                    message: `Failed to load Flashcards.`,
                });
            }
        };
        loadData();
    }, []);

    /**
     * Handles closing the modal and resetting the state.
     */
    const handleCloseModal = () => {
        setCardReversed(false);
        setCurrentFlashcardIndex(0);
        setOpen(false);
    };

    /**
     * Handles closing the flashcard and moving to the next one or closing the modal if it's the last flashcard.
     */
    const handleCloseFlashcard = () => {
        setCardReversed(false);
        if (currentFlashcardIndex < flashcards.length - 1) {
            setCurrentFlashcardIndex(currentFlashcardIndex + 1);
        } else {
            setCurrentFlashcardIndex(0);
            setOpen(false);
        }
    };

    return (
        <>
            {flashcards.length > 0 && (
                <StyledModal
                    open={open && flashcards.length > 0}
                    onClose={handleCloseModal}
                >
                    <Box>
                        <FlashcardPaper
                            flashcard={flashcards[currentFlashcardIndex]}
                            cardReversed={cardReversed}
                            setCardReversed={setCardReversed}
                            setRefreshTimestamp={() => { }}
                            handleClose={handleCloseFlashcard}
                        />
                        <StyledPagination
                            count={flashcards.length}
                            page={currentFlashcardIndex + 1}
                            boundaryCount={flashcards.length}
                            size="large"
                            onChange={(_, page) => setCurrentFlashcardIndex(page - 1)}
                            hidePrevButton
                            hideNextButton
                            renderItem={(item) => {
                                const flashcardRating = item.page != null ? flashcards[item.page - 1].rating : null;
                                return (
                                    <StyledPaginationItem
                                        {...item}
                                        flashcardRating={flashcardRating}
                                    />
                                )
                            }}
                        />
                    </Box>

                </StyledModal>
            )}
        </>
    );
};

export default LearningSessionModal;

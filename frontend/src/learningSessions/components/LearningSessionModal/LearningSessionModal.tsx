import { useState, useEffect } from "react";
import type { JSX } from "react";
import apiClient from "../../../core/apiClient";
import { useAlertContext } from "../../../core/store/AlertContext";
import FlashcardPaper from "../../../flashcards/components/SingleFlashcardModal/FlashcardPaper";
import type { Flashcard } from "../../../flashcards/types";
import { StyledModal } from "../../../flashcards/components/SingleFlashcardModal/styles";
import { Box, Pagination, PaginationItem, Typography } from "@mui/material";
import { theme } from "../../../core/theme";
import { FlashcardRating } from "../../../flashcards/constants";



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

    const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
    const [currentFlashcardIndex, setCurrentFlashcardIndex] = useState(0);

    /**
     * Fetches objects list from API.
     */
    useEffect(() => {
        const loadData = async () => {
            try {
                // TODO - fetch only flashcards ids and ratings, then fetch flashcard details one by one when needed, to avoid loading all flashcards at once
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

    const [cardReversed, setCardReversed] = useState(false);

    const handleCloseModal = () => {
        setCardReversed(false);
        setCurrentFlashcardIndex(0);
        setOpen(false);
    };

    const handleCloseFlashcard = () => {
        setCardReversed(false);
        if (currentFlashcardIndex < flashcards.length - 1) {
            setCurrentFlashcardIndex(currentFlashcardIndex + 1);
        } else {
            setCurrentFlashcardIndex(0);
            setOpen(false);
        }
    };

    const getFlashcardRatingColor = (rating: FlashcardRating | null) => {
        switch (rating) {
            case FlashcardRating.EASY:
                return theme.palette.primary.ratingEasyDark;
            case FlashcardRating.MEDIUM:
                return theme.palette.primary.ratingMediumDark;
            case FlashcardRating.HARD:
                return theme.palette.primary.ratingHardDark;
            default:
                return theme.palette.primary.light;
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
                        <Pagination
                            count={flashcards.length}
                            page={currentFlashcardIndex + 1}
                            boundaryCount={flashcards.length}
                            size="large"
                            onChange={(event, page) => setCurrentFlashcardIndex(page - 1)}
                            hidePrevButton
                            hideNextButton
                            renderItem={(item) => {
                                const flashcardRating = item.page != null ? flashcards[item.page - 1].rating : null;
                                return (
                                    <PaginationItem
                                        {...item}
                                        sx={{
                                            color: "white",
                                            bgcolor: getFlashcardRatingColor(flashcardRating),
                                            "&:hover": {
                                                bgcolor: getFlashcardRatingColor(flashcardRating),
                                                filter: "brightness(0.9)",
                                            },
                                            "&.Mui-selected": {
                                                bgcolor: getFlashcardRatingColor(flashcardRating),
                                                color: "white",
                                                border: `2px solid ${theme.palette.primary.dark}`,
                                            },
                                            "&.Mui-selected:hover": {
                                                bgcolor: getFlashcardRatingColor(flashcardRating),
                                                filter: "brightness(0.9)",
                                            },
                                        }}
                                    />
                                )
                            }}
                            sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                mt: 2,
                                // backgroundColor: theme.palette.primary.contrastText,
                                // border: `3px solid ${theme.palette.primary.dark}`,
                                borderRadius: 0,
                                padding: '4px'
                            }}
                        />
                    </Box>

                </StyledModal>
            )}
        </>
    );
};

export default LearningSessionModal;

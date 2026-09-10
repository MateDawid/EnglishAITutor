import { Pagination, PaginationItem } from '@mui/material';
import { styled } from '@mui/material/styles';
import { FlashcardRating } from "../../flashcards/constants";

export const StyledPagination = styled(Pagination)(({ theme }) => ({
    display: 'flex',
    justifyContent: 'center',
    marginTop: 8,
    borderRadius: 0,
    padding: 0
}));

export const StyledPaginationItem = styled(PaginationItem)<{ flashcardRating: FlashcardRating | null }>(({ theme, flashcardRating }) => {
    const getBackgroundColor = () => {
        switch (flashcardRating) {
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
    const bgColor = getBackgroundColor();
    
    return {
        color: "white",
        backgroundColor: bgColor,
        "&:hover": {
            backgroundColor: bgColor,
            filter: "brightness(0.9)",
        },
        "&.Mui-selected": {
            backgroundColor: bgColor,
            color: "white",
            border: `2px solid ${theme.palette.primary.dark}`,
        },
        "&.Mui-selected:hover": {
            backgroundColor: bgColor,
            filter: "brightness(0.9)",
        },
    };
});

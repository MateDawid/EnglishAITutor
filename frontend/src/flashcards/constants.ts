export const FlashcardRating ={
    NOT_RATED: 0,
    EASY: 1,
    MEDIUM: 2,
    HARD: 3,
} as const;

export type FlashcardRatingValue = (typeof FlashcardRating)[keyof typeof FlashcardRating];

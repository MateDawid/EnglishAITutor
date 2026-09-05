from enum import IntEnum


class DatabaseRating(IntEnum):
    """
    Enum representing ratings for Flashcards given by users in the database.

    Choices:
        EASY: Rating value of 1, indicating that the user finds the flashcard easy.
        MEDIUM: Rating value of 2, indicating that the user finds the flashcard of medium difficulty.
        HARD: Rating value of 3, indicating that the user finds the flashcard
    """

    EASY = 1
    MEDIUM = 2
    HARD = 3


class RatingFilter(IntEnum):
    """
    Enum representing rating filter choices in the flashcard list view.

    Choices:
        NOT_RATED: Rating value of 0, indicating that the user has not rated the flashcard.
        EASY: Rating value of 1, indicating that the user finds the flashcard easy.
        MEDIUM: Rating value of 2, indicating that the user finds the flashcard of medium difficulty.
        HARD: Rating value of 3, indicating that the user finds the flashcard hard.
    """

    NOT_RATED = 0
    EASY = DatabaseRating.EASY
    MEDIUM = DatabaseRating.MEDIUM
    HARD = DatabaseRating.HARD

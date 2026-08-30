from fastapi.openapi.models import Example

from flashcards.models.db_user_rating import Rating

RATING_EXAMPLES = {
    "easy": Example(value=Rating.EASY, summary="Easy"),
    "medium": Example(value=Rating.MEDIUM, summary="Medium"),
    "hard": Example(value=Rating.HARD, summary="Hard"),
}

from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    """
    Schema for Flashcard rating response.
    """

    rating_changed: bool

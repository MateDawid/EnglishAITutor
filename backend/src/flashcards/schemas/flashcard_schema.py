import uuid

from pydantic import BaseModel, ConfigDict

from flashcards.models.db_flashcard import PartOfSpeech
from flashcards.models.db_user_rating import Rating


class FlashcardSchema(BaseModel):
    """
    Schema for Flashcard database instance.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    word: str
    meaning: str
    part_of_speech: PartOfSpeech
    example: str | None = None
    user_rating: Rating | None = None

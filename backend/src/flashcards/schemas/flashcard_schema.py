import uuid

from pydantic import BaseModel, ConfigDict

from flashcards.enums import DatabaseRating
from flashcards.models.db_flashcard import PartOfSpeech


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
    rating: DatabaseRating | None = None

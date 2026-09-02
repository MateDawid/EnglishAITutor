import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, query_expression

from flashcards.enums import DatabaseRating
from utils.database import Base


class PartOfSpeech(str, Enum):
    """
    Enum representing the parts of speech for English words.
    """

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    NUMERAL = "numeral"
    PROPER_NOUN = "proper noun"


class DbFlashcard(Base):
    """
    Represents an English word flashcard in the database.

    Attributes:
        id (uuid.UUID): The unique identifier for the flashcard.
        word (str): The English word on the flashcard.
        meaning (str): The meaning of the English word.
        part_of_speech (PartOfSpeech): The part of speech of the English word.
        example (str): An example sentence using the English word.
        user_rating (Rating | None): The rating given by the user for the flashcard, if any.
    """

    __tablename__ = "flashcards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word: Mapped[str] = mapped_column(String(120), nullable=False)
    meaning: Mapped[str] = mapped_column(String(500), nullable=False)
    part_of_speech: Mapped[PartOfSpeech] = mapped_column(
        SqlEnum(PartOfSpeech, name="part_of_speech_enum"),
        nullable=False,
    )
    example: Mapped[str] = mapped_column(String(500), nullable=True)
    user_rating: Mapped[DatabaseRating | None] = query_expression()

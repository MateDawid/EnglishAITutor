import uuid
from enum import Enum

from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import Base


class Rating(int, Enum):
    """
    Enum representing ratings for Flashcards given by users in the database.
    """

    EASY = 1
    MEDIUM = 2
    HARD = 3


class DbUserRating(Base):
    """
    Represents ratings for Flashcards given by users in the database.
    """

    __tablename__ = "user_ratings"

    flashcard_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("flashcards.id"),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
    )
    rating: Mapped[Rating] = mapped_column(
        SqlEnum(Rating, name="rating_enum"),
        nullable=False,
    )

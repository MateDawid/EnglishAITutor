import uuid

from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from flashcards.enums import DatabaseRating
from utils.database import Base


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
    rating: Mapped[DatabaseRating] = mapped_column(
        SqlEnum(DatabaseRating, name="rating_enum"),
        nullable=False,
    )

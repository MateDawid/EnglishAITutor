import uuid
from datetime import datetime, UTC

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

## todo - regenerate migrations

class DbUser(Base):
    """
    Represents a user in the database.

    Attributes:
        id (uuid.UUID): The unique identifier for the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

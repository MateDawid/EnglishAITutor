from datetime import UTC, datetime

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class DbUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(UUID, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

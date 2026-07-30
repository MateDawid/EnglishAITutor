import uuid
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from utils.database import Base


class DbTestItem(Base):
    """
    Generic test model for pagination and sorting testing.
    """

    __tablename__ = "test_items"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False, default=0)


class TestItemSchema(BaseModel):
    """
    Generic test schema for pagination and sorting testing.
    """

    id: uuid.UUID
    name: str
    category: str
    priority: int = 0

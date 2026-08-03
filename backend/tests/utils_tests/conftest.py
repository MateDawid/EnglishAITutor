import uuid
from pydantic import BaseModel
from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from utils.database import Base
from enum import Enum


class EnumChoice(str, Enum):
    VALUE1 = "value1"
    VALUE2 = "value2"


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
    enum_field: Mapped[EnumChoice | None] = mapped_column(
        SqlEnum(EnumChoice, name="enum_field"),
        default=None,
        nullable=True,
    )


class TestItemSchema(BaseModel):
    """
    Generic test schema for pagination and sorting testing.
    """

    id: uuid.UUID
    name: str
    category: str
    priority: int = 0
    enum_field: EnumChoice | None = None

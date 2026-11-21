import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreateSchema(BaseModel):
    """Schema for creating a conversation."""

    title: str = Field(max_length=200)


class ConversationSchema(BaseModel):
    """Schema for a conversation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str | None
    created_at: datetime
    updated_at: datetime

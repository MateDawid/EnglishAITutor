import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationSchema(BaseModel):
    """Schema for a conversation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str | None
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    """
    Base schema for user-related data.
    """
    email: EmailStr = Field(max_length=120)
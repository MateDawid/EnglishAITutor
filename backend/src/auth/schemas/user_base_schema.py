from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    email: EmailStr = Field(max_length=120)
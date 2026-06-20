from auth.schemas.user_base_schema import UserBaseSchema
from pydantic import Field


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8)
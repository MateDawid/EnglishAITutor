from auth.schemas.user_base_schema import UserBaseSchema
from pydantic import Field


class UserCreateSchema(UserBaseSchema):
    """
    Schema for creating a new user, extending the base user schema with password fields.
    """

    password_1: str = Field(min_length=8)
    password_2: str = Field(min_length=8)

import uuid

from auth.schemas.user_base_schema import UserBaseSchema
from pydantic import ConfigDict


class UserRetrieveSchema(UserBaseSchema):
    """
    Schema for retrieving user information.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
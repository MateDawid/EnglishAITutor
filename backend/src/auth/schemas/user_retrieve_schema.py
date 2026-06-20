from auth.schemas.user_base_schema import UserBaseSchema
from pydantic import ConfigDict


class UserRetrieveSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
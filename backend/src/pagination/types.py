from typing import TypeVar

from pydantic import BaseModel

from utils.database import Base


SchemaType = TypeVar("SchemaType", bound=BaseModel)
DbModelType = TypeVar("DbModelType", bound=Base)

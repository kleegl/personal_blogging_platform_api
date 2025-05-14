from typing import List
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# create/update
class TagSchema(BaseSchema):
    name: str


# create/update
class PostSchema(BaseSchema):
    title: str | None = None
    content: str | None = None

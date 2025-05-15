from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseSchema):
    name: str


class TagCreateSchema(TagBase):
    pass


class TagUpdateSchema(BaseSchema):
    name: str | None = None


class TagResponse(TagBase):
    id: int
    pass


class PostBase(BaseSchema):
    title: str
    content: str


class PostCreateSchema(PostBase):
    tags: List[TagCreateSchema]


class PostUpdateSchema(BaseSchema):
    title: str | None = None
    content: str | None = None
    tags: List[TagUpdateSchema] | None = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse]

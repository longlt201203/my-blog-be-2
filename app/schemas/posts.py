from typing_extensions import Annotated
from bson import ObjectId
from pydantic import BaseModel, Field

from ..schemas.common import PyMongoObjectId

class Post(BaseModel):
    # _id: ObjectId
    id: PyMongoObjectId
    tags: list[str]
    title: str
    thumbnail_img: str
    thumbnail_description: str
    author: str | None = None
    created_at: str | None = None
    last_update: str | None = None
    content: str | None = None

class CreatePostDto(BaseModel):
    tags: list[str]
    title: str
    thumbnail_img: str
    thumbnail_description: str
    content: str

class UpdatePostDto(CreatePostDto):
    pass
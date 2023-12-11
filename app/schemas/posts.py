from pydantic import BaseModel, Field

from ..schemas.common import PyObjectId

class Post(BaseModel):
    id: PyObjectId = Field(alias="_id")
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
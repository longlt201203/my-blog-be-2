from typing import List
from bson import ObjectId
from pymongo import database
from ..schemas.posts import *

class PostsService:
    def __init__(self, db_conn: database.Database):
        self.posts_collection = db_conn["posts"]

    def get_posts(self) -> List[Post]:
        posts = list(self.posts_collection.find())
        return posts
    
    def get_post_by_id(self, id: str) -> Post | None:
        if (not ObjectId.is_valid(id)):
            return None
        post = self.posts_collection.find_one({ "_id": ObjectId(id) })
        return post
    
    def create_post(self, dto: CreatePostDto):
        data = dto.model_dump()
        data.setdefault("id", ObjectId())
        result = self.posts_collection.insert_one(data)
        return result.inserted_id
    
    def update_post(self, id: str, dto: UpdatePostDto) -> Post | None:
        if (not ObjectId.is_valid(id)):
            return None
        post = self.posts_collection.find_one_and_update({ "_id" : ObjectId(id) }, dto.model_dump(exclude=["_id"]))
        return post
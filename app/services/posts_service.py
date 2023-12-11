from typing import List
from bson import ObjectId
from pymongo import ReturnDocument, database

from app.schemas.common import GetManyResponseDto
from ..schemas.posts import *

class PostsService:
    def __init__(self, db_conn: database.Database):
        self.posts_collection = db_conn["posts"]

    def get_posts(self, page: int, perPage: int) -> GetManyResponseDto[Post]:
        posts = list(
            self.posts_collection
                .find()
                .limit(perPage)
                .skip((page-1)*perPage)
            )
        
        count_documents = self.posts_collection.count_documents({})

        result = GetManyResponseDto[Post](
            data=posts,
            page=page,
            perPage=perPage,
            nextPage=page+1 if page*perPage < count_documents else None,
            prevPage=page-1 if page-1 > 0 else None,
            totalPage=count_documents//perPage + (1 if count_documents%perPage > 0 else 0)
        )

        return result
    
    def get_post_by_id(self, id: str) -> Post | None:
        if (not ObjectId.is_valid(id)):
            return None
        post = self.posts_collection.find_one({ "_id": ObjectId(id) })
        return post
    
    def create_post(self, dto: CreatePostDto):
        data = dto.model_dump()
        data.setdefault("id", ObjectId())
        result = self.posts_collection.insert_one(data)
        post = self.get_post_by_id(result.inserted_id.__str__())
        return post
    
    def update_post(self, id: str, dto: UpdatePostDto) -> Post | None:
        if (not ObjectId.is_valid(id)):
            return None
        post = self.posts_collection.find_one_and_update({ "_id" : ObjectId(id) }, {
            "$set" : dto.model_dump(exclude=["_id"]),
        }, return_document=ReturnDocument.AFTER)
        return post
    
    def delete_post(self, id: str) -> Post | None:
        if (not ObjectId.is_valid(id)):
            return None
        post = self.posts_collection.find_one_and_delete({ "_id": ObjectId(id) })
        return post
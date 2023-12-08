from typing import Annotated, List
from fastapi import APIRouter, Body, Request, status
from fastapi.responses import JSONResponse
from ..services.posts_service import PostsService
from ..schemas.posts import *
from ..schemas.common import *

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/{id}", response_model=Post, responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse}})
async def get_post(id: str, req: Request):
    posts_service = PostsService(req.app.database)
    post = posts_service.get_post_by_id(id)
    if (post == None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message": f"Post {id} is not found"})
    return post

@router.get("/", response_model=List[Post])
def get_posts(req: Request):
    posts_service = PostsService(req.app.database)
    posts = posts_service.get_posts()
    return posts

@router.post("/")
def create_post(dto: CreatePostDto, req: Request):
    posts_service = PostsService(req.app.database)
    posts_service.create_post(dto)

@router.patch("/{id}", response_model=Post, responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse}})
def update_post(id: str, dto: Annotated[UpdatePostDto, Body], req: Request):
    posts_service = PostsService(req.app.database)
    post = posts_service.update_post(id, dto)
    if (post == None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message": f"Post {id} is not found"})
    return post

@router.delete("/{id}")
def delete_post(id: str):
    return "OK"
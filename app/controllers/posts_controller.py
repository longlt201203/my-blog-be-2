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

@router.get("/", response_model=GetManyResponseDto[Post])
def get_posts(req: Request, page: int | None = None, perPage: int | None = None):
    posts_service = PostsService(req.app.database)
    posts = posts_service.get_posts(
        perPage=10 if perPage == None else perPage,
        page=1 if page == None else page
    )
    return posts

@router.post("/", response_model=Post)
def create_post(dto: CreatePostDto, req: Request):
    posts_service = PostsService(req.app.database)
    return posts_service.create_post(dto)

@router.patch("/{id}", response_model=Post, responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse}})
def update_post(id: str, dto: Annotated[UpdatePostDto, Body], req: Request):
    posts_service = PostsService(req.app.database)
    post = posts_service.update_post(id, dto)
    if (post == None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message": f"Post {id} is not found"})
    return post

@router.delete("/{id}", response_model=Post, responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse}})
def delete_post(id: str, req: Request):
    posts_service = PostsService(req.app.database)
    post = posts_service.delete_post(id)
    if (post == None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message": f"Post {id} is not found"})
    return post
from fastapi import APIRouter, Request, Depends, HTTPException, status, Response, Path
from typing import Annotated
from news.schemas import PostCreate, PostRead
from news.dependencies import get_news_service
from news.service import NewsService
from users.dependencies import check_user_have_access_token
from auth.tokens_check_dependencies import jwt_refresh_token_check_dependency, jwt_access_token_check_dependency
news_router = APIRouter(prefix="/news", tags=["news"])

@news_router.post("/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_user_have_access_token),
                                                                                      Depends(jwt_refresh_token_check_dependency),
                                                                                      Depends(jwt_access_token_check_dependency)])
async def create_news(post: PostCreate, request: Request,
                      news_service: NewsService = Depends(get_news_service)):
    return await news_service.create_post(post, request)

@news_router.get("/read/{post_id}")
async def read_post(post_id: Annotated[int, Path()],request: Request, news_service: NewsService = Depends(get_news_service)):
    return await news_service.read_post(request, post_id)

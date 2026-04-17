from fastapi import APIRouter, Request, Depends, HTTPException, status, Response, Path
from sqlalchemy.sql.annotation import Annotated
from news.schemas import PostCreate, PostRead
from news.dependencies import get_news_service
from news.service import NewsService

news_router = APIRouter(prefix="/news", tags=["news"])

@news_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_news(post: PostCreate, request: Request,
                      news_service: NewsService = Depends(get_news_service)):
    return await news_service.create_post(post, request)

# @news_router.get("/read/{post_id}")
# async def read_post(post_id: Annotated[int, Path()], news_service: NewsService = Depends(get_news_service)):
#     return news_service.read_post(post_id)

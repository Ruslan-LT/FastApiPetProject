from sqlalchemy.ext.asyncio import AsyncSession
from news.service import NewsService
from fastapi import Depends
from src.database import session_dependency


def get_news_service(session: AsyncSession = Depends(session_dependency)) -> NewsService:
    return NewsService(session)
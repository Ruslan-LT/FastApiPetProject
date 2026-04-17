from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, Request
from .models import PostORM, PostQueryORM
from .repository import NewsRepository
from news.schemas import PostCreate, PostRead
from fastapi import status
from users.repository import UserRepository
from users.security import COOKIE_SESSION_ID_KEY, COOKIE_ADMIN_KEY

class NewsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.news_repository = NewsRepository(session)
        self.user_repository = UserRepository(session)

    async def create_post(self, post: PostCreate, request: Request):
        user_session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        if user_session_id == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        user_orm_obj = await self.user_repository.get_user(user_session_id)
        res = user_orm_obj.scalar_one_or_none()
        post_obj = PostORM(**post.model_dump(), user_id=res.user.id)
        await self.news_repository.create_post(post_obj)
        await self.session.flush()
        if request.cookies.get(COOKIE_ADMIN_KEY) != 'True':
            post_query_obj = PostQueryORM(post_id=post_obj.id)
            await self.news_repository.add_post_to_query(post_query_obj)
        await self.session.commit()
        await self.session.refresh(post_obj)
        return PostRead.model_validate(post_obj)





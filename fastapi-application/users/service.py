from news.models import PostQueryORM
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from news.repository import NewsRepository
from users.schemas import UserCreate, UserRead, UserInDB, UserUpdate
from users.models import UserORM, SessionORM
from .convert_models import convert_user_model
from users.security import get_password_hash, generate_session_id,get_session_id
from .repository import UserRepository
from fastapi import status
from news.schemas import PostRead
from users.security import COOKIE_SESSION_ID_KEY, COOKIE_ADMIN_KEY, COOKIE_USER_ID_KEY, COOKIE_SESSION_EXPIRES_KEY,\
    COOKIE_LIST
from datetime import datetime, timezone, timedelta

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(self.session)
        self.news_repository = NewsRepository(self.session)

    async def create_user_account(self, user: UserCreate, response, request):
        if request.cookies.get(COOKIE_SESSION_ID_KEY):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered", )
        data = user.model_dump()
        hash_password = await get_password_hash(data.pop("password"))
        user_db = UserORM(
            **data,
            hashed_password=hash_password
        )
        await self.user_repository.create_user(user_db)
        await self.session.commit()
        await self.session.refresh(user_db)
        return await convert_user_model(user_db, UserRead)

    async def login_user_account(self, auth_user, response):
        conflict_exc = HTTPException(status.HTTP_409_CONFLICT, "User already authenticated")
        res = await self.user_repository.check_user_session_exists(auth_user.username)
        user_obj = res.scalar_one_or_none()
        if not user_obj.user_session:
            session_id = await generate_session_id()
            user_session = SessionORM(session_id=session_id, user_id=auth_user.id)
            await self.user_repository.create_user_session(user_session)
            user_orm_obj = await self.user_repository.check_user_is_admin(auth_user.username)
            user_obj = user_orm_obj.scalar_one_or_none()
            if user_obj.admin:
                response.set_cookie(COOKIE_ADMIN_KEY, 'True', max_age=86400, expires=86400)
            else:
                response.set_cookie(COOKIE_ADMIN_KEY, 'False', max_age=86400, expires=86400)
            await self.session.commit()
            response.set_cookie(COOKIE_SESSION_ID_KEY, str(session_id), max_age=86400, expires=86400)
            response.set_cookie(COOKIE_USER_ID_KEY, auth_user.id, max_age=86400, expires=86400)
            response.set_cookie(COOKIE_SESSION_EXPIRES_KEY, datetime.now(timezone.utc) + timedelta(days=1))
            return {
                'result': 'ok'
            }
        raise conflict_exc

    async def logout_user_account(self, response, request,):
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        if session_id == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        res = await self.user_repository.get_user(session_id)
        session_obj = res.scalar_one_or_none()
        username = session_obj.user.username
        await self.user_repository.delete_user_session(session_id)
        await self.session.commit()
        for cookie in COOKIE_LIST:
            response.delete_cookie(cookie)
        return {
            'Message:': f'Bye {username}!'
        }

    async def read_auth_user_account(self,  request, session_id:str):
        orm_obj = await self.user_repository.get_user(session_id)
        res = orm_obj.scalar()
        auth_user = res.user
        return await convert_user_model(auth_user, UserRead)


    async def update_user_account(self, user_update:UserUpdate, session_id:str):
        res = await self.user_repository.get_user(session_id)
        session_obj = res.scalar_one_or_none()
        user = session_obj.user
        for name, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, name, value)
        await self.session.commit()
        await self.session.refresh(user)
        return await convert_user_model(user, UserRead)

    async def delete_post_by_user(self, request, post_id):
        post_orm_obj = await self.news_repository.read_post(post_id)
        post = post_orm_obj.scalar_one_or_none()
        user_id = int(request.cookies.get(COOKIE_USER_ID_KEY))
        if not post or post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.query:
            await self.news_repository.remove_from_query(post.id)
        await self.news_repository.delete_post(post.id)
        await self.session.commit()

    async def update_post_by_user(self, post_id, PostUpdateObj, request):
        post_orm_obj = await self.news_repository.read_post(post_id)
        post = post_orm_obj.scalar_one_or_none()
        if post == None or post.user_id != int(request.cookies.get(COOKIE_USER_ID_KEY)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.query:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post in query")
        for name, value in PostUpdateObj.model_dump(exclude_unset=True).items():
            setattr(post, name, value)
        if request.cookies.get(COOKIE_ADMIN_KEY) != 'True':
            query_obj = PostQueryORM(post_id=post.id)
            await self.news_repository.add_post_to_query(query_obj)
        await self.session.commit()
        await self.session.refresh(post)
        return await convert_user_model(post, PostRead)





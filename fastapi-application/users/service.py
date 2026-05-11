from news.models import PostQueryORM
from fastapi import HTTPException, status, Header, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from news.repository import NewsRepository
from users.schemas import UserCreate, UserRead, UserInDB, UserUpdate, Token
from users.models import UserORM,JWT_RefreshToken
from .convert_models import convert_user_model
from users.security import get_password_hash
from auth.helpers import create_access_token, create_refresh_token
from .repository import UserRepository
from news.schemas import PostRead
from users.security import  COOKIE_ADMIN_KEY,COOKIE_LIST, COOKIE_ACCESS_TOKEN_KEY, COOKIE_REFRESH_TOKEN_KEY
from datetime import datetime, timezone, timedelta
from auth.utils import encode_jwt, decode_jwt
from fastapi.security import HTTPAuthorizationCredentials

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(self.session)
        self.news_repository = NewsRepository(self.session)

    async def create_user_account(self, user: UserCreate, response, request):
        if request.cookies.get(COOKIE_ACCESS_TOKEN_KEY):
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


    async def login_user_account_jwt(self, auth_user, response: Response, request: Request):
        if request.cookies.get(COOKIE_ACCESS_TOKEN_KEY) != None:
            raise HTTPException(status.HTTP_409_CONFLICT, "User already authenticated")
        access_token = await create_access_token(auth_user)
        refresh_token = await create_refresh_token(auth_user)
        jwt_refresh_obj = JWT_RefreshToken(token=refresh_token, user_id=auth_user.id)
        await self.user_repository.add_jwt_refresh_token(jwt_refresh_obj)
        await self.session.commit()
        user_obj = await self.user_repository.check_user_is_admin(auth_user.username)
        user = user_obj.scalar_one_or_none()
        if user.admin:
            response.set_cookie(COOKIE_ADMIN_KEY, 'True')
        else:
            response.set_cookie(COOKIE_ADMIN_KEY, 'False')
        response.set_cookie(
            key=COOKIE_ACCESS_TOKEN_KEY,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        response.set_cookie(
            key=COOKIE_REFRESH_TOKEN_KEY,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return Token(access_token=access_token,
                     refresh_token= refresh_token,)

    async def logout_user_account(self, response, request,):
        access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        if access_token == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        user_id = int((await decode_jwt(access_token))['sub'])
        await self.user_repository.delete_jwt_refresh_token_by_user_id(user_id)
        await self.session.commit()
        res = await self.user_repository.get_user(user_id)
        user_obj = res.scalar_one_or_none()
        username = user_obj.username
        for cookie in COOKIE_LIST:
            response.delete_cookie(cookie)
        return {
            'Message:': f'Bye {username}!'
        }

    async def read_auth_user_account(self,  request: Request,):
        access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        user_id = int((await decode_jwt(access_token))['sub'])
        orm_obj = await self.user_repository.get_user(user_id)
        auth_user = orm_obj.scalar()
        return await convert_user_model(auth_user, UserRead)


    async def update_user_account(self, user_update:UserUpdate, request: Request):
        access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        user_id = int((await decode_jwt(access_token))['sub'])
        res = await self.user_repository.get_user(user_id)
        user = res.scalar_one_or_none()
        for name, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, name, value)
        await self.session.commit()
        await self.session.refresh(user)
        return await convert_user_model(user, UserRead)

    async def delete_post_by_user(self, request, post_id):
        post_orm_obj = await self.news_repository.read_post(post_id)
        post = post_orm_obj.scalar_one_or_none()
        access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        user_id = int((await decode_jwt(access_token))['sub'])
        if not post or post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.query:
            await self.news_repository.remove_from_query(post.id)
        await self.news_repository.delete_post(post.id)
        await self.session.commit()

    async def update_post_by_user(self, post_id, PostUpdateObj, request):
        post_orm_obj = await self.news_repository.read_post(post_id)
        post = post_orm_obj.scalar_one_or_none()
        access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        user_id = int((await decode_jwt(access_token))['sub'])
        if post == None or post.user_id != user_id:
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

    async def refresh_jwt_access(self, request: Request, response: Response,):
        jwt_access_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
        if jwt_access_token is not None:
            response.delete_cookie(COOKIE_ACCESS_TOKEN_KEY)
            user_id = (await decode_jwt(request.cookies.get(COOKIE_REFRESH_TOKEN_KEY)))['sub']
            new_access_token = await create_access_token(user_id=user_id)
            response.set_cookie(COOKIE_ACCESS_TOKEN_KEY, new_access_token)
            return {'new_access_token': new_access_token}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )





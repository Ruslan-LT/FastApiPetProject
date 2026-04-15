from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import UserCreate, UserRead, UserInDB, UserUpdate
from users.models import UserORM, SessionORM
from .convert_models import convert_user_model
from users.security import get_password_hash, generate_session_id
from .repository import UserRepository
from fastapi import status
from users.security import COOKIE_SESSION_ID_KEY

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(self.session)

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
            await self.session.commit()
            response.set_cookie(COOKIE_SESSION_ID_KEY, str(session_id), max_age=86400, expires=86400)
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
        response.delete_cookie(COOKIE_SESSION_ID_KEY)

        return {
            'Message:': f'Bye {username}'
        }

    async def read_auth_user_account(self,  request):
        session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
        if session_id == None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        orm_obj = await self.user_repository.get_user(session_id)
        res = orm_obj.scalar()
        auth_user = res.user
        return await convert_user_model(auth_user, UserRead)






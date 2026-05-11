import uuid
from pwdlib import PasswordHash
from fastapi import Request, HTTPException, Depends, status, Form
from typing import Annotated
from .convert_models import convert_user_model
from users.models import UserORM
from users.schemas import UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from auth.utils import decode_jwt
from src.database import session_dependency
from jwt.exceptions import InvalidTokenError
from users.repository import UserRepository
from auth.utils import encode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
COOKIE_SESSION_ID_KEY = 'web-app-session-id'
COOKIE_ADMIN_KEY = 'web-app-admin'
COOKIE_USER_ID_KEY = 'web-app-user_id'
COOKIE_SESSION_EXPIRES_KEY = 'web-app-session-expires'
COOKIE_USERNAME_KEY = 'web-app-username'
COOKIE_REFRESH_TOKEN_KEY = 'web-app-refresh-token'
COOKIE_ACCESS_TOKEN_KEY = 'web-app-access-token'

COOKIE_LIST = [COOKIE_ADMIN_KEY, COOKIE_REFRESH_TOKEN_KEY, COOKIE_ACCESS_TOKEN_KEY]

async def generate_session_id() -> str:
    return str(uuid.uuid4())

async def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return password_hash.hash(password)

async def get_current_token_payload(token:str):
    try:
        payload = await decode_jwt(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=repr(e))

async def get_current_user(payload:dict = Depends(get_current_token_payload),
                           session: AsyncSession = Depends(session_dependency)):
    user_repository = UserRepository(session)
    user_id = payload.get('sub')
    user_orm = await user_repository.get_user_by_id(user_id)
    if not user_orm:
        raise HTTPException(status_code=401, detail="Token Invalid")
    return await convert_user_model(user_orm, UserRead)


async def get_auth_username(request: Request,
                            session:Annotated[AsyncSession,Depends(session_dependency)],
                            username: str = Form(),
                            password: str = Form(),) -> UserRead:
    from users.orm import get_user_from_orm
    unauth_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    user_db = await get_user_from_orm(username, session)
    if not user_db:
        raise unauth_exeption

    if not await verify_password(password, user_db.hashed_password):
        raise unauth_exeption

    return UserRead(**user_db.model_dump())


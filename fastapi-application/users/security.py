import uuid

from pwdlib import PasswordHash
from fastapi import Request, HTTPException, Depends, status
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from users.schemas import UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency

security = HTTPBasic()
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
COOKIE_SESSION_ID_KEY = 'web-app-session-id'

async def generate_session_id() -> str:
    return str(uuid.uuid4())

async def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return password_hash.hash(password)


async def get_auth_username(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)],
                            session:Annotated[AsyncSession,Depends(session_dependency)]) -> UserRead:
    from users.orm import get_user_from_orm
    unauth_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    user_db = await get_user_from_orm(credentials.username, session)
    if not user_db:
        raise unauth_exeption

    if not await verify_password(credentials.password, user_db.hashed_password):
        raise unauth_exeption


    return UserRead(**user_db.model_dump())


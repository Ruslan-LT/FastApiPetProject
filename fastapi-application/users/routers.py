from typing import Annotated, Any
from fastapi import (Depends,APIRouter, Response)
from users.orm import create_user_with_orm, create_session_from_orm
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from users.schemas import UserInDB, UserCreate, UserRead
from users.security import security, get_password_hash, verify_password,\
                            get_auth_username,COOKIE_SESSION_ID_KEY,generate_session_id

user_router = APIRouter(tags=["users"],
                        prefix="/users",)

@user_router.post("/register", response_model=UserRead)
async def create_user(user: UserCreate, session:Annotated[AsyncSession, Depends(session_dependency)]):
    result = await create_user_with_orm(user, session)
    return result

@user_router.post("/login")
async def user_login(response: Response, auth_user:Annotated[UserRead, Depends(get_auth_username)],
                     session:Annotated[AsyncSession, Depends(session_dependency)]):
    session_id = await generate_session_id()
    await create_session_from_orm(session_id, auth_user.id,session)
    response.set_cookie(COOKIE_SESSION_ID_KEY, str(session_id))
    return {
        'result': 'ok'
    }

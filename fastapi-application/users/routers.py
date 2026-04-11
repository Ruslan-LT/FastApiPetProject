from typing import Annotated, Any
from fastapi import (Depends, APIRouter, Response, Request, HTTPException, status)
from users.orm import create_user_with_orm, create_session_from_orm, delete_session_from_orm,check_session_exists,get_username
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
    conflict_exc = HTTPException(status.HTTP_409_CONFLICT, "User already authenticated")
    res = await check_session_exists(session, auth_user.username)
    session_id = await generate_session_id()
    if res:
        await create_session_from_orm(session_id, auth_user.id,session)
        response.set_cookie(COOKIE_SESSION_ID_KEY, str(session_id))
        return {
            'result': 'ok'
        }
    raise conflict_exc

@user_router.post("/logout")
async def user_logout(response: Response,
                      request: Request,
                      session:Annotated[AsyncSession, Depends(session_dependency)]):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    if session_id == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    username = await get_username(session_id, session)
    await delete_session_from_orm(session_id, session)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    return {
        'Message:': f'Bye {username}'
    }




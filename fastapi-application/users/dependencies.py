from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import session_dependency
from users.service import UserService
from fastapi import Request, Response, Depends, HTTPException
from .security import COOKIE_ACCESS_TOKEN_KEY

def get_user_service(session: AsyncSession = Depends(session_dependency)):
    return UserService(session)

async def check_user_have_access_token(request: Request, response: Response,):
    if request.cookies.get(COOKIE_ACCESS_TOKEN_KEY) == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from users.service import UserService


def get_user_service(session: AsyncSession = Depends(session_dependency)):
    return UserService(session)

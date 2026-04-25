from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from users.schemas import UserCreate, UserRead, UserInDB
from users.models import UserORM, SessionORM
from .convert_models import convert_user_model

async def get_user_from_orm(username: str, session: AsyncSession):
    query = select(UserORM).where(UserORM.username == username)
    res = await session.execute(query)
    user_db = res.scalar_one_or_none()
    if user_db:
        return await convert_user_model(user_db, UserInDB)







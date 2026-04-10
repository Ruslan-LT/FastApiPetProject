from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import UserCreate, UserRead, UserInDB
from users.models import UserORM, SessionORM
from .convert_models import convert_user_model
from users.security import get_password_hash

async def create_user_with_orm(user: UserCreate, session: AsyncSession):
    data = user.model_dump()

    hash_password = await get_password_hash(data.pop("password"))
    user_db = UserORM(
        **data,
        hashed_password=hash_password
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return await convert_user_model(user_db, UserRead)

async def get_user_from_orm(username: str, session: AsyncSession):
    query = select(UserORM).where(UserORM.username == username)
    res = await session.execute(query)
    user_db = res.scalar_one_or_none()
    if user_db:
        return await convert_user_model(user_db, UserInDB)


async def create_session_from_orm(session_id, user_id, session: AsyncSession):
    user_session = SessionORM(session_id=session_id, user_id=user_id)
    session.add(user_session)
    await session.commit()


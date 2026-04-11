from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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

async def check_session_exists(session: AsyncSession, username):
    q = select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.user_session))
    req = await session.execute(q)
    user_obj = req.scalar_one_or_none()
    if not user_obj.user_session:
        return True

async def create_session_from_orm(session_id, user_id, session: AsyncSession):
    user_session = SessionORM(session_id=session_id, user_id=user_id)
    session.add(user_session)
    await session.commit()

async def delete_session_from_orm(session_id, session: AsyncSession):
    smt = delete(SessionORM).where(SessionORM.session_id == session_id)
    await session.execute(smt)
    await session.commit()

async def get_username(session_id, session):
    smt = select(SessionORM).where(SessionORM.session_id == session_id).options(joinedload(SessionORM.user))
    res = await session.execute(smt)
    session_obj = res.scalar_one_or_none()
    if session_obj:
        return session_obj.user.username



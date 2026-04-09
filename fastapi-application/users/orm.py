from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated
from src.database import session_dependency
from users.schemas import UserCreate
from users.models import UserORM
from .convert_models import convert_user_model

async def create_user_with_orm(user: UserCreate, session: AsyncSession):
    data = user.model_dump()

    password = data.pop("password")
    user_db = UserORM(
        **data,
        hashed_password=password
    )

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return await convert_user_model(user_db)



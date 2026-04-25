from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from news.models import PostORM, PostQueryORM

class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_min_query_id(self):
        min_id_orm = await self.session.execute(select(func.min(PostQueryORM.id)))
        min_id = min_id_orm.scalar_one_or_none()
        return min_id

    async def read_query_post(self, id: int):
            stmt = await self.session.execute(select(PostORM).join(PostQueryORM).where(PostQueryORM.id == id))
            return stmt

    async def read_post(self, id: int):
        stmt = await self.session.execute(select(PostORM).where(PostORM.id == id).options(joinedload(PostORM.query)))
        return stmt

    async def remove_from_query(self, id: int):
        smt = await self.session.execute(delete(PostQueryORM).where(PostQueryORM.id == id))
        return smt

    async def delete_post(self, id: int):
        stmt = await self.session.execute(delete(PostORM).where(PostORM.id == id))
        return stmt








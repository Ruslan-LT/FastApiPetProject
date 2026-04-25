from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from news.models import PostORM, PostQueryORM
from users.models import UserORM, SessionORM

class NewsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(self, post: PostORM):
        return self.session.add(post)

    async def add_post_to_query(self, post: PostQueryORM):
        return self.session.add(post)

    async def read_post(self, id: int):
        res = await self.session.execute(select(PostORM).where(PostORM.id == id).options(joinedload(PostORM.query)))
        return res

    async def delete_post(self, id: int):
        res = await self.session.execute(delete(PostORM).where(PostORM.id == id))

    async def remove_from_query(self, id: int):
        smt = await self.session.execute(delete(PostQueryORM).where(PostQueryORM.post_id == id))
        return smt




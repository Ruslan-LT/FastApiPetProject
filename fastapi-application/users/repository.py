from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from users.models import UserORM, SessionORM


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserORM):
        return self.session.add(user)

    async def get_user(self, session_id):
        res = await self.session.execute(select(SessionORM).where(SessionORM.session_id == session_id).options(joinedload(SessionORM.user)))
        return res

    async def check_user_session_exists(self, username):
        res = await self.session.execute(select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.user_session)))
        return res

    async def create_user_session(self, user_session: SessionORM):
        self.session.add(user_session)

    async def delete_user_session(self, session_id):
        res = await self.session.execute(delete(SessionORM).where(SessionORM.session_id == session_id))
        return res

class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user_is_admin(self, username):
        smt = await self.session.execute(select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.admin)))
        return smt






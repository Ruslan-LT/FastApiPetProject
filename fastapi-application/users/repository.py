from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from users.models import UserORM, JWT_RefreshToken


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserORM):
        return self.session.add(user)

    async def get_user(self, session_id):
        res = await self.session.execute(select(UserORM).where(UserORM.id == session_id))
        return res

    async def check_user_session_exists(self, username):
        res = await self.session.execute(select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.user_session)))
        return res

    async def check_user_is_admin(self, username):
        smt = await self.session.execute(select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.admin)))
        return smt

    async def get_user_by_id(self, id):
        res = await self.session.execute(select(UserORM).where(UserORM.id == id))
        return

    async def add_jwt_refresh_token(self, jwt_refresh_token: JWT_RefreshToken):
        return self.session.add(jwt_refresh_token)

    async def get_user_by_username(self, username):
        stmt = await self.session.execute(select(UserORM).where(UserORM.username == username))

    async def get_refresh_token_by_username(self, username):
        stmt = await self.session.execute(select(UserORM).where(UserORM.username == username).options(joinedload(UserORM.jwt_refresh)))

    async def delete_jwt_refresh_token_by_user_id(self, user_id):
        stmt = await self.session.execute(delete(JWT_RefreshToken).where(JWT_RefreshToken.user_id == user_id))

    async def delete_jwt_refresh_token_by_token_body(self, token):
        stmt = await  self.session.execute(delete(JWT_RefreshToken).where(JWT_RefreshToken.token == token))










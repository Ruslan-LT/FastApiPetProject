from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, HTTPException, status
from news.service import PostRead
from admin.repository import AdminRepository


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.AdminRepository = AdminRepository(session)

    async def read_post(self, request: Request, post_id: int|None = None):
        if post_id == None:
            min_id = await self.AdminRepository.get_min_query_id()
            if min_id == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The table with posts in the queue is empty")
            else:
                post_orm_obj = await self.AdminRepository.read_query_post(min_id)
                post = post_orm_obj.scalar_one_or_none()
                return PostRead.model_validate(post)
        else:
            post_orm_obj = await self.AdminRepository.read_post(post_id)
            post = post_orm_obj.scalar_one_or_none()
            if post == None or not post.query:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
            return PostRead.model_validate(post)


    async def remove_post_from_query(self, post_id):
        if post_id == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail="post_id is required")
        post_orm_obj = await self.AdminRepository.read_post(post_id)
        post_obj = post_orm_obj.scalar_one_or_none()
        if post_obj == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        else:
            query_oqj = post_obj.query
            if query_oqj == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not in queue")
            else:
                query_id = post_obj.query.id
                await self.AdminRepository.remove_from_query(query_id)
                return post_obj.id


    async def accept_post(self,post_id: int|None):
        await self.remove_post_from_query(post_id)
        await self.session.commit()
        return {'message': 'Accepted'}


    async def decline_post(self,post_id: int|None):
        post_id = await self.remove_post_from_query(post_id)
        await self.session.commit()
        await self.AdminRepository.delete_post(post_id)
        await self.session.commit()
        return {'message': 'Declined'}

    async def delete_post(self,post_id):
        if post_id == None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail="post_id is required")
        post_orm_obj = await self.AdminRepository.read_post(post_id)
        post_obj = post_orm_obj.scalar_one_or_none()
        if post_obj == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post_obj.query:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post in queue!")
        await self.AdminRepository.delete_post(post_id)
        await self.session.commit()
        return {'message': 'Deleted'}

















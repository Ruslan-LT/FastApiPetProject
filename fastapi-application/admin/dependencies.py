from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.security import COOKIE_ADMIN_KEY
from src.database import session_dependency
from admin.service import AdminService

def admin_check(request:Request):
    if request.cookies.get(COOKIE_ADMIN_KEY) != 'True':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access rights to this resource')


def get_admin_service(session: AsyncSession = Depends(session_dependency)) -> AdminService:
    return AdminService(session)
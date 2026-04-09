from time import time
import uuid
from typing import Annotated, Any
from fastapi import Depends, FastAPI, HTTPException, status, Request, Header, Cookie, APIRouter
from fastapi.responses import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import secrets
from users.orm import create_user_with_orm
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from users.schemas import UserInDB, UserCreate, UserRead

security = HTTPBasic()
user_router = APIRouter(tags=["users"],
                        prefix="/users",)



@user_router.post("/register", response_model=UserRead)
async def create_user(user: UserCreate, session:Annotated[AsyncSession, Depends(session_dependency)]):
    result = await create_user_with_orm(user, session)
    return result

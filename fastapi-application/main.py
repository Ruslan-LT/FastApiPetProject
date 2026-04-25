from fastapi import FastAPI, Request, Depends, Response
from typing import Annotated
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from users.routers import user_router
from news.routers import news_router
from admin.routers import admin_router
from datetime import datetime, timezone
from users.security import COOKIE_SESSION_EXPIRES_KEY, COOKIE_LIST, COOKIE_SESSION_ID_KEY
from users.repository import UserRepository
from src.database import session_dependency

app = FastAPI()
app.include_router(user_router)
app.include_router(news_router)
app.include_router(admin_router)

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   allow_headers=['*'],
                   allow_credentials=True,)

@app.middleware('http')
async def session_expire_check_middleware(request: Request, call_next,):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    if session_id:
        session = session_dependency()
        user_repository = UserRepository(session=session)
        time_now = datetime.now(timezone.utc)
        session_expire_time_str = str(request.cookies.get(COOKIE_SESSION_EXPIRES_KEY))
        try:
            session_expires = datetime.fromisoformat(session_expire_time_str)
        except ValueError:
            return await call_next(request)
        if session_expires < time_now:
            response = Response(status_code=401)
            for cookie in COOKIE_LIST:
                response.delete_cookie(cookie)
            await user_repository.delete_user_session(session_id)
            return response
    response = await call_next(request)
    return response



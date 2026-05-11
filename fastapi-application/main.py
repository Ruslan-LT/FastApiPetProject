from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from users.routers import user_router
from news.routers import news_router
from admin.routers import admin_router
app = FastAPI()
app.include_router(user_router)
app.include_router(news_router)
app.include_router(admin_router)

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=['*'],
                   allow_headers=['*'],
                   allow_credentials=True,
                   expose_headers=["Authorization"])


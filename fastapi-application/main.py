from fastapi import FastAPI
from users.routers import user_router
from news.routers import news_router

app = FastAPI()
app.include_router(user_router)
app.include_router(news_router)





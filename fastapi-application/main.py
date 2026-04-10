from fastapi import FastAPI
from users.routers import user_router

app = FastAPI()
app.include_router(user_router)




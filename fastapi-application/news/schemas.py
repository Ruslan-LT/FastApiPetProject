from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str

class PostRead(Post):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostCreate(Post):
    ...

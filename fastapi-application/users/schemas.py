from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

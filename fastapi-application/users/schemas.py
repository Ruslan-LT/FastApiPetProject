from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str

class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    ...

class UserUpdatePartial(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

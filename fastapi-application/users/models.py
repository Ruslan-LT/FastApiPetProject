from sqlalchemy import String, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum

from src.base import Base

class RoleEnum(Enum):
    admin = "admin"
    user = "user"

class UserORM(Base):
    __tablename__ = 'users'
    username:Mapped[str] = mapped_column(String(35))
    hashed_password:Mapped[str] = mapped_column(String(35))
    first_name:Mapped[str] = mapped_column(String(30))
    last_name:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(35))
    role:Mapped[RoleEnum] = mapped_column(default=RoleEnum.user,
                                          server_default='user')
    disabled:Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        UniqueConstraint('username'),
    )
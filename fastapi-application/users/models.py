from sqlalchemy import String,Integer, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from src.base import Base

class RoleEnum(Enum):
    admin = "admin"
    user = "user"


class UserORM(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(35))
    hashed_password:Mapped[str] = mapped_column(String(150))
    first_name:Mapped[str] = mapped_column(String(30))
    last_name:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(35))
    role:Mapped[RoleEnum] = mapped_column(default=RoleEnum.user,
                                          server_default='user')
    disabled:Mapped[bool] = mapped_column(default=False,
                                          server_default='false')

    user_session:Mapped['SessionORM'] = relationship(back_populates='user',)

    __table_args__ = (
        UniqueConstraint('username'),
    )

class SessionORM(Base):
    __tablename__ = "sessions"
    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user:Mapped['UserORM'] = relationship(back_populates='user_session')
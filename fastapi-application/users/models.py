from datetime import datetime, timedelta
from sqlalchemy import DateTime
from black import timezone
from sqlalchemy import String,Integer, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from admin.models import AdminORM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from news.models import PostORM
    from admin.models import AdminORM

from src.base import Base

class UserORM(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(35))
    hashed_password:Mapped[str] = mapped_column(String(150))
    first_name:Mapped[str] = mapped_column(String(30))
    last_name:Mapped[str] = mapped_column(String(30))
    email:Mapped[str] = mapped_column(String(35))
    disabled:Mapped[bool] = mapped_column(default=False,
                                          server_default='false')

    admin:Mapped['AdminORM'] = relationship( back_populates='user', uselist=False)

    posts:Mapped[list['PostORM']] = relationship(back_populates='user',)

    jwt_refresh:Mapped['JWT_RefreshToken'] = relationship(back_populates='user',)

    __table_args__ = (
        UniqueConstraint('username'),
    )


class JWT_RefreshToken(Base):
    __tablename__ = "jwt_refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token:Mapped[str] = mapped_column(String)

    user:Mapped['UserORM'] = relationship(back_populates='jwt_refresh')

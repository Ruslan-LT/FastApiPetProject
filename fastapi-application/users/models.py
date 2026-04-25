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

    user_session:Mapped['SessionORM'] = relationship(back_populates='user', uselist=False)

    __table_args__ = (
        UniqueConstraint('username'),
    )

class SessionORM(Base):
    __tablename__ = "sessions"
    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1),
        index=True
    )

    user:Mapped['UserORM'] = relationship(back_populates='user_session')
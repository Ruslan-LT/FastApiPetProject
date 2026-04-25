from datetime import datetime, timedelta
from sqlalchemy import DateTime, Column
from black import timezone
from sqlalchemy import String,Integer, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import UserORM
    from admin.models import AdminORM

from src.base import Base

class PostORM(Base):
    __tablename__ = 'post'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title:Mapped[str] = mapped_column(String(50))
    content:Mapped[str] = mapped_column(String(1500))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc))

    user:Mapped['UserORM'] = relationship(back_populates='posts')

    query:Mapped['PostQueryORM'] = relationship(back_populates='post', uselist=False)

class PostQueryORM(Base):
    __tablename__ = 'post_query'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id:Mapped[int] = mapped_column(ForeignKey('post.id'), unique=True)

    post:Mapped['PostORM'] = relationship(back_populates='query')


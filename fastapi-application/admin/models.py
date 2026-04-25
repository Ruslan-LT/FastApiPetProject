from sqlalchemy import String,Integer, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from src.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import UserORM

class AdminORM(Base):
    __tablename__ = 'admins'
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user:Mapped['UserORM'] = relationship(back_populates='admin')
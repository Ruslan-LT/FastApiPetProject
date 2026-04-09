from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
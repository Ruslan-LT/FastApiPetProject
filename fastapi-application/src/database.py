from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession, async_sessionmaker, \
    async_scoped_session
from src.config import settings
from asyncio import current_task

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)

async def session_dependency():
    async with async_session_factory() as session:
        yield session
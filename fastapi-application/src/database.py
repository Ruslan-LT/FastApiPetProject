from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession, async_sessionmaker, \
    async_scoped_session
from src.config import settings
from asyncio import current_task

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)


async_session_factory = async_sessionmaker(async_engine)


async def get_scoped_session():
    session = async_scoped_session(
        async_session_factory,
        scopefunc=current_task,
    )
    return session

async def session_dependency():
    session = await get_scoped_session()
    yield session
    await session.close()

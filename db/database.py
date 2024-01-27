from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
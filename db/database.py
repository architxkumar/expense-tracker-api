import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

engine: AsyncEngine = create_async_engine(os.getenv('DATABASE_URL'), echo=True)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session_maker() as session:
        yield session

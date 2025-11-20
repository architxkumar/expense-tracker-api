import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# For local development, `.env` file is loaded whereas in docker container the environment variables is derived from the container environment
load_dotenv()

database_user = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')
database_name = os.getenv('DATABASE_NAME')

database_url = f'postgresql+asyncpg://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'
engine: AsyncEngine = create_async_engine(database_url, echo=True)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session_maker() as session:
        yield session

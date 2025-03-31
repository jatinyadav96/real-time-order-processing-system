import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, future=True, echo=True, pool_size=10,  # Max connections
                             max_overflow=5, )
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# For Kafka Consumer
async def get_consumer_db():
    async with AsyncSessionLocal() as session:
        yield session

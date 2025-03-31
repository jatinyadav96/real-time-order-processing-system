import asyncio
import logging

from app.database import engine
from app.models import Base


async def init_db():
    logging.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created successfully.")


if __name__ == "__main__":
    asyncio.run(init_db())


#/app/database/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends


DATABASE_URL = 'postgresql+asyncpg://user_api:4564@localhost/my_first_app_db'

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

#Создание типа для зависимости чтобы не писать депендс каждый раз
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]

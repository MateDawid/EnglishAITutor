import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator, Any, Generator

from main import app
from config import settings
from database import Base, get_db

# Set up a test database URL
admin_engine = create_engine(
   settings.admin_database_url, isolation_level="AUTOCOMMIT"
)

# Create an engine and sessionmaker bound to the test database
engine = create_async_engine(settings.database_url)
TestingSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    """
    Create the test database if it doesn't exist.
    """
    with admin_engine.connect() as connection:
        print(f"Creating test database: {settings.database_url.split('/')[-1]}")
        try:
            connection.execute(
                text(f"CREATE DATABASE {settings.database_url.split('/')[-1]}")
            )
        except ProgrammingError:
            print("Database already exists, continuing...")



@pytest.mark.asyncio(loop_scope="session")
async def setup_test_database():
    create_test_database()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session for each test and roll it back after the test.

    Yields:
        AsyncSession: A SQLAlchemy async session for the test.
    """
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = TestingSession(bind=connection)

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    """
    Fixture to provide a TestClient for the FastAPI app.

    Yields:
        AsyncClient: An AsyncClient instance for the FastAPI app.
    """

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

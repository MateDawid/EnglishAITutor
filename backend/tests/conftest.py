import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from typing import AsyncGenerator
from sqlalchemy.pool import NullPool

from auth.models import DbUser
from auth.services.current_user_service import get_current_user_from_db
from factories.user import UserFactory
from main import app
from config import settings
from utils.database import Base, get_db

pytest_plugins = ["anyio"]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Configures AnyIO to run tests using the asyncio backend.

    Returns:
        str: String indicating the name of the backend.
    """
    return "asyncio"


@pytest.fixture(scope="session")
def test_engine() -> AsyncEngine:
    """
    Creates and returns the asynchronous SQLAlchemy engine used by tests.

    The engine uses a NullPool to ensure connections are not reused between tests.

    Returns:
        AsyncEngine: The asynchronous engine used by tests.
    """
    return create_async_engine(settings.database_url, poolclass=NullPool)


@pytest.fixture(scope="session")
async def setup_database(test_engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """
    Creates all database tables before the test session starts and
    remove them after the test session completes.

    Args:
        test_engine: The asynchronous SQLAlchemy engine used for testing.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session(
    test_engine: AsyncEngine,
    setup_database: AsyncGenerator[None, None],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Creates new, isolated database session for a test.

    A transaction is started before the test and rolled back afterward
    to ensure each test runs against a clean database state.

    Args:
        test_engine (AsyncEngine): The asynchronous SQLAlchemy engine used for testing.
        setup_database (AsyncGenerator[None, None]): Fixture ensuring the database schema exists.

    Yields:
        AsyncSession: A transactional asynchronous database session.
    """

    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    """
    Creates an HTTP client configured to use the test application.

    The application's database dependency is overridden so all requests
    use the test database session provided by the fixture.

    Args:
        db_session: The database session used during the test.

    Yields:
        AsyncClient: An HTTPX asynchronous client for interacting with the FastAPI application.
    """

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> DbUser:
    """
    Creates test DbUser in the database.

    Args:
        db_session (AsyncSession): The database session used during the test.

    Returns:
        DbUser: Created test user.
    """
    UserFactory._meta.sqlalchemy_session = db_session

    user = UserFactory.build(
        email="test@example.com",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def authenticated_client(
    client: AsyncClient,
    test_user: DbUser,
):
    """
    Creates an authenticated HTTP client for testing.

    The client's authentication is overridden to always use the provided test user.

    Args:
        client (AsyncClient): The HTTP client used during the test.
        test_user (DbUser): The test user to authenticate as.

    Yields:
        AsyncClient: An authenticated HTTP client.
    """

    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user_from_db] = override_get_current_user

    yield client

    app.dependency_overrides.pop(get_current_user_from_db, None)

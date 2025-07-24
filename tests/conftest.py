"""Pytest configuration and fixtures."""
import asyncio
from collections.abc import AsyncGenerator, Generator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.database import Base, get_db
from app.main import app

# Import all models to ensure they are registered with Base.metadata
from app.models import Category, Todo, User  # noqa: F401
from app.models.todo import TodoStatus
from app.utils.security import get_password_hash

# Test database URL - Using check_same_thread for SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a new database session for a test."""
    # Create test engine with StaticPool for SQLite in-memory
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client."""
    from httpx import ASGITransport

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield async_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_db(async_session: AsyncSession) -> AsyncSession:
    """Provide test database session."""
    return async_session


@pytest_asyncio.fixture(scope="function")
async def test_user(async_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash=get_password_hash("TestPassword123!"),
        name="Test User",
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def auth_headers(test_user: User, app_settings) -> dict:
    """Create authentication headers with JWT token."""
    access_token_expires = timedelta(minutes=app_settings.access_token_expire_minutes)
    access_token = jwt.encode(
        {
            "sub": str(test_user.id),
            "exp": datetime.now(UTC) + access_token_expires,
        },
        app_settings.secret_key.get_secret_value(),
        algorithm=app_settings.algorithm,
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def create_expired_token(app_settings):
    """Factory to create expired JWT tokens for testing."""
    def _create_token(data: dict):
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        expire = datetime.now(UTC) - timedelta(hours=1)  # Already expired
        data.update({"exp": expire})

        return jwt.encode(
            data,
            app_settings.secret_key.get_secret_value(),
            algorithm=app_settings.algorithm
        )
    return _create_token


@pytest_asyncio.fixture(scope="function")
async def test_category(
    async_session: AsyncSession,
    test_user: User
) -> Category:
    """Create a test category."""
    from app.models.category import Category

    category = Category(
        id=uuid4(),
        user_id=test_user.id,
        name="Test Category",
        color="#FF5733"
    )
    async_session.add(category)
    await async_session.commit()
    await async_session.refresh(category)
    return category


@pytest_asyncio.fixture(scope="function")
async def test_todo(
    async_session: AsyncSession,
    test_user: User,
    test_category: Category
) -> Todo:
    """Create a test todo."""
    from app.models.todo import Todo

    todo = Todo(
        id=uuid4(),
        title="Test Todo",
        description="Test Description",
        user_id=test_user.id,
        category_id=test_category.id,
        status=TodoStatus.OPEN
    )
    async_session.add(todo)
    await async_session.commit()
    await async_session.refresh(todo)
    return todo


@pytest_asyncio.fixture(scope="function")
async def create_test_todos(
    async_session: AsyncSession,
    test_user: User,
    test_category: Category
):
    """Create multiple test todos for testing lists/filters."""
    from app.models.todo import Todo

    todos = [
        Todo(
            title="Important Task",
            description="Very important",
            user_id=test_user.id,
            category_id=test_category.id,
            status=TodoStatus.OPEN
        ),
        Todo(
            title="Completed Task",
            description="Already done",
            user_id=test_user.id,
            status=TodoStatus.COMPLETED
        ),
        Todo(
            title="Future Task",
            due_date=datetime.now(UTC) + timedelta(days=30),
            user_id=test_user.id,
            status=TodoStatus.OPEN
        )
    ]

    for todo in todos:
        async_session.add(todo)
    await async_session.commit()

    return todos


@pytest_asyncio.fixture(scope="function")
async def other_user_todo(
    async_session: AsyncSession
) -> Todo:
    """Create a todo belonging to another user."""
    from app.models.todo import Todo

    # Create another user
    other_user = User(
        id=uuid4(),
        email="other@example.com",
        password_hash=get_password_hash("OtherPassword123!"),
        name="Other User",
        is_active=True
    )
    async_session.add(other_user)
    await async_session.flush()

    # Create their todo
    todo = Todo(
        title="Other User's Todo",
        user_id=other_user.id
    )
    async_session.add(todo)
    await async_session.commit()

    return todo


@pytest_asyncio.fixture
async def create_test_categories(
    async_session: AsyncSession,
    test_user: User
):
    """Create multiple test categories."""
    from app.models.category import Category

    categories = [
        Category(name="Personal", color="#FF0000", user_id=test_user.id),
        Category(name="Work", color="#00FF00", user_id=test_user.id),
        Category(name="Shopping", color="#0000FF", user_id=test_user.id),
    ]

    for category in categories:
        async_session.add(category)
    await async_session.commit()

    return categories


@pytest_asyncio.fixture
async def empty_category(
    async_session: AsyncSession,
    test_user: User
):
    """Create a category with no todos."""
    from app.models.category import Category

    category = Category(
        name="Empty Category",
        user_id=test_user.id
    )
    async_session.add(category)
    await async_session.commit()
    await async_session.refresh(category)
    return category


@pytest_asyncio.fixture
async def category_with_todos(
    async_session: AsyncSession,
    test_user: User
):
    """Create a category with several todos."""
    from app.models.category import Category
    from app.models.todo import Todo

    category = Category(
        name="Category with Todos",
        user_id=test_user.id
    )
    async_session.add(category)
    await async_session.flush()

    todos = [
        Todo(
            title=f"Todo {i}",
            user_id=test_user.id,
            category_id=category.id,
            status=(
                TodoStatus.COMPLETED if i % 2 == 0
                else TodoStatus.OPEN
            )  # Every other todo is completed
        )
        for i in range(5)
    ]

    for todo in todos:
        async_session.add(todo)

    await async_session.commit()
    await async_session.refresh(category)

    # Refresh todos to ensure they have IDs
    for todo in todos:
        await async_session.refresh(todo)

    return {"category": category, "todos": todos}


@pytest_asyncio.fixture
async def category_with_many_todos(
    async_session: AsyncSession,
    test_user: User
):
    """Create a category with many todos for pagination testing."""
    from app.models.category import Category
    from app.models.todo import Todo

    category = Category(
        name="Category with Many Todos",
        user_id=test_user.id
    )
    async_session.add(category)
    await async_session.flush()

    todos = [
        Todo(
            title=f"Todo {i:03d}",
            user_id=test_user.id,
            category_id=category.id
        )
        for i in range(25)
    ]

    for todo in todos:
        async_session.add(todo)

    await async_session.commit()
    await async_session.refresh(category)
    return category

@pytest.fixture
def exhaust_rate_limit():
    """Helper to exhaust rate limit for a user."""
    async def _exhaust(client: AsyncClient, headers: dict):
        # Make requests until we hit 429
        for _ in range(200):  # Safety limit
            response = await client.get(
                "/api/v1/todos",
                headers=headers
            )
            if response.status_code == 429:
                return
        raise Exception("Failed to hit rate limit")

    return _exhaust

@pytest_asyncio.fixture
async def second_user_headers(
    client: AsyncClient,
    async_session: AsyncSession
):
    """Create a second user and return auth headers."""
    from app.schemas.user import UserCreate
    from app.services.auth import create_user

    # Create second user
    user_data = UserCreate(
        email="second@example.com",
        password="password123",
        full_name="Second User"
    )
    await create_user(async_session, user_data)

    # Login and get token
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "second@example.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def app_settings():
    """Get current settings for rate limit values."""
    return settings

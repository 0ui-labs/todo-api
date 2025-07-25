"""Unit tests for TodoService."""
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoFilter, TodoUpdate
from app.services.todo import TodoService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = AsyncMock(spec=AsyncSession)
    mock.commit = AsyncMock()
    mock.refresh = AsyncMock()
    mock.add = MagicMock()
    return mock


@pytest.fixture
def todo_service(mock_db):
    """Create a TodoService instance with mock db."""
    return TodoService(mock_db)


@pytest.fixture
def sample_user_id():
    """Create a sample user ID."""
    return uuid4()


@pytest.fixture
def sample_category():
    """Create a sample category."""
    return Category(
        id=uuid4(),
        user_id=uuid4(),
        name="Work",
        color="#FF5733"
    )


@pytest.fixture
def sample_todo(sample_user_id, sample_category):
    """Create a sample todo."""
    return Todo(
        id=uuid4(),
        user_id=sample_user_id,
        title="Test Todo",
        description="Test Description",
        status=TodoStatus.OPEN,
        due_date=datetime.now(),
        category_id=sample_category.id,
        category=sample_category,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        completed_at=None,
        deleted_at=None
    )


@pytest.fixture
def sample_todo_create():
    """Create a sample TodoCreate schema."""
    return TodoCreate(
        title="New Todo",
        description="New Description",
        due_date=datetime.now() + timedelta(days=1),  # Future date
        category_id=uuid4()
    )


@pytest.fixture
def sample_todo_update():
    """Create a sample TodoUpdate schema."""
    return TodoUpdate(
        title="Updated Todo",
        status=TodoStatus.IN_PROGRESS
    )


class TestTodoService:
    """Test cases for TodoService."""

    async def test_create_todo_success(
        self, todo_service, mock_db, sample_user_id, sample_todo_create
    ):
        """Test successful todo creation."""
        # Mock refresh to simulate database returning the created todo
        mock_db.refresh = AsyncMock()

        # Call the method
        result = await todo_service.create_todo(sample_user_id, sample_todo_create)

        # Verify the result
        assert result is not None
        assert result.title == sample_todo_create.title
        assert result.user_id == sample_user_id

        # Verify todo was created
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

        # Verify the todo object was created correctly
        todo_arg = mock_db.add.call_args[0][0]
        assert isinstance(todo_arg, Todo)
        assert todo_arg.user_id == sample_user_id
        assert todo_arg.title == sample_todo_create.title
        assert todo_arg.description == sample_todo_create.description

    async def test_get_todo_success(
        self, todo_service, mock_db, sample_todo, sample_user_id
    ):
        """Test getting a todo by ID."""
        # Mock query result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_todo
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await todo_service.get_todo(sample_todo.id, sample_user_id)

        # Verify result
        assert result == sample_todo

    async def test_get_todo_not_found(self, todo_service, mock_db, sample_user_id):
        """Test getting a non-existent todo."""
        # Mock query result - no todo found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await todo_service.get_todo(uuid4(), sample_user_id)

        # Verify result
        assert result is None

    async def test_get_todos_with_pagination(
        self, todo_service, mock_db, sample_user_id, sample_todo
    ):
        """Test getting todos with pagination."""
        # Mock count query result
        count_result = MagicMock()
        count_result.scalar_one.return_value = 10

        # Mock todos query result
        todos_result = MagicMock()
        todos_result.scalars.return_value.all.return_value = [sample_todo]

        # Set up execute to return different results for count and todos queries
        mock_db.execute.side_effect = [count_result, todos_result]

        # Call the method
        todos, total = await todo_service.get_todos(sample_user_id, limit=5, offset=0)

        # Verify results
        assert len(todos) == 1
        assert todos[0] == sample_todo
        assert total == 10

    async def test_get_todos_with_filter(
        self, todo_service, mock_db, sample_user_id, sample_todo
    ):
        """Test getting todos with filters."""
        # Mock results
        count_result = MagicMock()
        count_result.scalar_one.return_value = 1

        todos_result = MagicMock()
        todos_result.scalars.return_value.all.return_value = [sample_todo]

        mock_db.execute.side_effect = [count_result, todos_result]

        # Create filter
        filter_params = TodoFilter(
            status=TodoStatus.OPEN,
            search="Test"
        )

        # Call the method
        todos, total = await todo_service.get_todos(
            sample_user_id,
            filter_params=filter_params
        )

        # Verify results
        assert len(todos) == 1
        assert total == 1

    async def test_get_todos_with_sort(
        self, todo_service, mock_db, sample_user_id, sample_todo
    ):
        """Test getting todos with sorting."""
        # Mock results
        count_result = MagicMock()
        count_result.scalar_one.return_value = 1

        todos_result = MagicMock()
        todos_result.scalars.return_value.all.return_value = [sample_todo]

        mock_db.execute.side_effect = [count_result, todos_result]

        # Call the method with sort parameters
        todos, total = await todo_service.get_todos(
            sample_user_id,
            sort_by="created_at",
            order="desc"
        )

        # Verify results
        assert len(todos) == 1
        assert total == 1

    async def test_update_todo_success(
        self, todo_service, mock_db, sample_todo, sample_user_id, sample_todo_update
    ):
        """Test successful todo update."""
        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo', return_value=sample_todo):
            # Call the method
            result = await todo_service.update_todo(
                sample_todo.id,
                sample_user_id,
                sample_todo_update
            )

            # Verify todo was updated
            assert result is not None
            assert mock_db.commit.called
            assert mock_db.refresh.called
            assert sample_todo.title == sample_todo_update.title
            assert sample_todo.status == sample_todo_update.status

    async def test_update_todo_status_to_completed(
        self, todo_service, mock_db, sample_todo, sample_user_id
    ):
        """Test updating todo status to completed sets completed_at."""
        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo', return_value=sample_todo):
            # Update to completed status
            update_data = TodoUpdate(status=TodoStatus.COMPLETED)

            # Call the method
            result = await todo_service.update_todo(
                sample_todo.id,
                sample_user_id,
                update_data
            )

            # Verify completed_at was set
            assert result is not None
            assert sample_todo.status == TodoStatus.COMPLETED
            assert sample_todo.completed_at is not None

    async def test_update_todo_not_found(
        self, todo_service, mock_db, sample_user_id, sample_todo_update
    ):
        """Test updating non-existent todo."""
        # Mock get_todo to return None
        with patch.object(todo_service, 'get_todo', return_value=None):
            # Call the method
            result = await todo_service.update_todo(
                uuid4(),
                sample_user_id,
                sample_todo_update
            )

            # Verify result
            assert result is None
            assert not mock_db.commit.called

    async def test_delete_todo_success(
        self, todo_service, mock_db, sample_todo, sample_user_id
    ):
        """Test successful todo deletion."""
        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo', return_value=sample_todo):
            # Call the method
            result = await todo_service.delete_todo(sample_todo.id, sample_user_id)

            # Verify todo was soft deleted
            assert result is True
            assert sample_todo.deleted_at is not None
            assert mock_db.commit.called

    async def test_delete_todo_not_found(self, todo_service, mock_db, sample_user_id):
        """Test deleting non-existent todo."""
        # Mock get_todo to return None
        with patch.object(todo_service, 'get_todo', return_value=None):
            # Call the method
            result = await todo_service.delete_todo(uuid4(), sample_user_id)

            # Verify result
            assert result is False
            assert not mock_db.commit.called

    async def test_get_todos_by_category(
        self, todo_service, mock_db, sample_user_id, sample_todo, sample_category
    ):
        """Test getting todos by category."""
        # Mock query result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_todo]
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await todo_service.get_todos_by_category(
            sample_user_id,
            sample_category.id
        )

        # Verify result
        assert len(result) == 1
        assert result[0] == sample_todo

    async def test_create_todo_database_error(
        self, todo_service, mock_db, sample_user_id, sample_todo_create
    ):
        """Test todo creation with database error."""
        # Mock database error on commit
        mock_db.commit.side_effect = IntegrityError("", "", "")

        # Should raise IntegrityError
        with pytest.raises(IntegrityError):
            await todo_service.create_todo(sample_user_id, sample_todo_create)

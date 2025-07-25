"""Unit tests for TodoService status change logic."""
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoUpdate
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


class TestTodoServiceStatusHandling:
    """Test cases for status change handling in TodoService."""

    async def test_update_status_to_completed_sets_timestamp(
        self, todo_service, mock_db, sample_user_id
    ):
        """Test that completed_at is set when status changes from OPEN to COMPLETED."""
        # Create a todo that is currently open
        existing_todo = Todo(
            id=uuid4(),
            user_id=sample_user_id,
            title="Test Todo",
            description="Test Description",
            status=TodoStatus.OPEN,
            completed_at=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo') as mock_get:
            # First call returns the existing todo, second call returns updated todo
            mock_get.side_effect = [existing_todo, existing_todo]

            # Update status to completed
            update_data = TodoUpdate(status=TodoStatus.COMPLETED)

            # Call the method
            await todo_service.update_todo(
                existing_todo.id,
                sample_user_id,
                update_data
            )

            # Verify completed_at was set
            assert existing_todo.status == TodoStatus.COMPLETED
            assert existing_todo.completed_at is not None
            # Verify the timestamp is recent (within last minute)
            time_diff = datetime.now(UTC) - existing_todo.completed_at
            assert time_diff.total_seconds() < 60

    async def test_update_status_from_completed_clears_timestamp(
        self, todo_service, mock_db, sample_user_id
    ):
        """Test completed_at cleared when status changes from COMPLETED to OPEN."""
        # Create a todo that is currently completed
        completed_time = datetime.now(UTC) - timedelta(hours=1)
        existing_todo = Todo(
            id=uuid4(),
            user_id=sample_user_id,
            title="Test Todo",
            description="Test Description",
            status=TodoStatus.COMPLETED,
            completed_at=completed_time,
            created_at=datetime.now(UTC) - timedelta(days=1),
            updated_at=datetime.now(UTC)
        )

        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo') as mock_get:
            # First call returns the existing todo, second call returns updated todo
            mock_get.side_effect = [existing_todo, existing_todo]

            # Update status back to open
            update_data = TodoUpdate(status=TodoStatus.OPEN)

            # Call the method
            await todo_service.update_todo(
                existing_todo.id,
                sample_user_id,
                update_data
            )

            # Verify completed_at was cleared
            assert existing_todo.status == TodoStatus.OPEN
            assert existing_todo.completed_at is None

    async def test_update_completed_todo_does_not_change_timestamp(
        self, todo_service, mock_db, sample_user_id
    ):
        """Test completed_at unchanged when updating completed todo."""
        # Create a todo that is already completed
        original_completed_time = datetime.now(UTC) - timedelta(hours=2)
        existing_todo = Todo(
            id=uuid4(),
            user_id=sample_user_id,
            title="Test Todo",
            description="Test Description",
            status=TodoStatus.COMPLETED,
            completed_at=original_completed_time,
            created_at=datetime.now(UTC) - timedelta(days=1),
            updated_at=datetime.now(UTC)
        )

        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo') as mock_get:
            # First call returns the existing todo, second call returns updated todo
            mock_get.side_effect = [existing_todo, existing_todo]

            # Update only the title, not the status
            update_data = TodoUpdate(title="Updated Title")

            # Call the method
            await todo_service.update_todo(
                existing_todo.id,
                sample_user_id,
                update_data
            )

            # Verify completed_at was NOT changed
            assert existing_todo.status == TodoStatus.COMPLETED
            assert existing_todo.completed_at == original_completed_time
            assert existing_todo.title == "Updated Title"

    async def test_update_non_status_field_preserves_completed_at(
        self, todo_service, mock_db, sample_user_id
    ):
        """Test completed_at unchanged when updating other fields of completed todo."""
        # Create a completed todo
        original_completed_time = datetime.now(UTC) - timedelta(days=1)
        existing_todo = Todo(
            id=uuid4(),
            user_id=sample_user_id,
            title="Test Todo",
            description="Test Description",
            status=TodoStatus.COMPLETED,
            completed_at=original_completed_time,
            due_date=datetime.now(UTC) + timedelta(days=7),
            created_at=datetime.now(UTC) - timedelta(days=2),
            updated_at=datetime.now(UTC)
        )

        # Mock get_todo to return the existing todo
        with patch.object(todo_service, 'get_todo') as mock_get:
            # First call returns the existing todo, second call returns updated todo
            mock_get.side_effect = [existing_todo, existing_todo]

            # Update multiple fields but not status
            update_data = TodoUpdate(
                title="New Title",
                description="New Description",
                due_date=datetime.now(UTC) + timedelta(days=14)
            )

            # Call the method
            await todo_service.update_todo(
                existing_todo.id,
                sample_user_id,
                update_data
            )

            # Verify fields were updated but completed_at preserved
            assert existing_todo.title == "New Title"
            assert existing_todo.description == "New Description"
            assert existing_todo.status == TodoStatus.COMPLETED
            assert existing_todo.completed_at == original_completed_time

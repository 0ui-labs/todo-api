"""Test TodoStatus validation in todos API."""
import pytest

from app.schemas.todo import TodoFilter, TodoStatus


class TestTodoStatusValidation:
    """Test that TodoStatus is properly validated."""

    def test_todo_filter_accepts_valid_status_enum(self) -> None:
        """Test that TodoFilter accepts valid TodoStatus enum values."""
        # Test with valid enum values
        filter1 = TodoFilter(status=TodoStatus.OPEN)
        assert filter1.status == TodoStatus.OPEN

        filter2 = TodoFilter(status=TodoStatus.IN_PROGRESS)
        assert filter2.status == TodoStatus.IN_PROGRESS

        filter3 = TodoFilter(status=TodoStatus.COMPLETED)
        assert filter3.status == TodoStatus.COMPLETED

    def test_todo_filter_accepts_valid_status_string(self) -> None:
        """Test that TodoFilter accepts valid status strings and converts them."""
        # Test with string values that should be converted to enum
        filter1 = TodoFilter(status="open")
        assert filter1.status == TodoStatus.OPEN

        filter2 = TodoFilter(status="in_progress")
        assert filter2.status == TodoStatus.IN_PROGRESS

        filter3 = TodoFilter(status="completed")
        assert filter3.status == TodoStatus.COMPLETED

    def test_todo_filter_rejects_invalid_status_string(self) -> None:
        """Test that TodoFilter rejects invalid status strings."""
        # Test with invalid status string
        with pytest.raises(ValueError) as exc_info:
            TodoFilter(status="invalid_status")

        # Should contain helpful error message
        assert "invalid_status" in str(exc_info.value).lower()

    def test_todo_filter_accepts_none_status(self) -> None:
        """Test that TodoFilter accepts None for status (no filter)."""
        filter_obj = TodoFilter(status=None)
        assert filter_obj.status is None

    def test_todo_filter_case_insensitive_status(self) -> None:
        """Test that TodoFilter handles case-insensitive status strings."""
        # Test various case combinations
        filter1 = TodoFilter(status="OPEN")
        assert filter1.status == TodoStatus.OPEN

        filter2 = TodoFilter(status="In_Progress")
        assert filter2.status == TodoStatus.IN_PROGRESS

        filter3 = TodoFilter(status="Completed")
        assert filter3.status == TodoStatus.COMPLETED

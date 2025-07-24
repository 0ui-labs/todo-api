"""Integration tests for caching functionality."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate
from app.services.cache import get_cache_service
from app.services.todo import TodoService


@pytest.mark.asyncio
async def test_todo_caching(
    async_session: AsyncSession,
    test_user,
    test_category
):
    """Test that todos are cached and invalidated properly."""
    todo_service = TodoService(async_session)
    cache_service = await get_cache_service()
    
    # Create a todo
    todo_data = TodoCreate(
        title="Test Cached Todo",
        description="This should be cached",
        category_id=test_category.id
    )
    todo = await todo_service.create_todo(test_user.id, todo_data)
    
    # First get_todo should hit the database
    result1 = await todo_service.get_todo(todo.id, test_user.id)
    assert result1 is not None
    assert result1.title == "Test Cached Todo"
    
    # Check if it's in cache
    cache_key = f"user:{test_user.id}:get_todo:todo_id:{todo.id}:user_id:{test_user.id}"
    cached = await cache_service.get("todos", cache_key)
    assert cached is not None  # Should be cached now
    
    # Second get_todo should hit the cache (but we can't easily verify this in integration test)
    result2 = await todo_service.get_todo(todo.id, test_user.id)
    assert result2 is not None
    assert result2.title == "Test Cached Todo"
    
    # Update the todo - should invalidate cache
    from app.schemas.todo import TodoUpdate
    update_data = TodoUpdate(title="Updated Cached Todo")
    updated = await todo_service.update_todo(todo.id, test_user.id, update_data)
    assert updated.title == "Updated Cached Todo"
    
    # Check that cache was invalidated
    cached_after_update = await cache_service.get("todos", cache_key)
    assert cached_after_update is None  # Should be invalidated
    
    # Clean up
    await cache_service.delete_pattern("todos", f"user:{test_user.id}:*")


@pytest.mark.asyncio
async def test_get_todos_caching(
    async_session: AsyncSession,
    test_user,
    test_category
):
    """Test that get_todos results are cached."""
    todo_service = TodoService(async_session)
    cache_service = await get_cache_service()
    
    # Create some todos
    for i in range(3):
        todo_data = TodoCreate(
            title=f"Todo {i}",
            description=f"Description {i}",
            category_id=test_category.id
        )
        await todo_service.create_todo(test_user.id, todo_data)
    
    # First get_todos should hit the database
    todos1, total1 = await todo_service.get_todos(test_user.id, limit=10, offset=0)
    assert total1 >= 3
    assert len(todos1) >= 3
    
    # Second get_todos with same params should be cached
    todos2, total2 = await todo_service.get_todos(test_user.id, limit=10, offset=0)
    assert total2 == total1
    assert len(todos2) == len(todos1)
    
    # Different params should not use cache
    todos3, total3 = await todo_service.get_todos(test_user.id, limit=5, offset=0)
    assert len(todos3) <= 5
    
    # Clean up
    await cache_service.delete_pattern("todos", f"user:{test_user.id}:*")
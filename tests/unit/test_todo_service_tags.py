"""Unit tests for todo service tag functionality."""

from uuid import uuid4

import pytest

from app.models.user import User
from app.schemas.tag import TagCreate
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services.tag import TagService
from app.services.todo import TodoService


@pytest.mark.asyncio
async def test_create_todo_with_tags(async_session, test_user: User):
    """Test creating a todo with tags."""
    # Create tags first
    tag_service = TagService(async_session)
    tag1 = await tag_service.create(TagCreate(name="urgent"))
    tag2 = await tag_service.create(TagCreate(name="work"))

    # Create todo with tags
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo with tags",
        description="This todo has tags",
        tag_ids=[tag1.id, tag2.id]
    )

    todo = await todo_service.create_todo(test_user.id, todo_data)

    assert todo.id is not None
    assert len(todo.tags) == 2
    tag_names = {tag.name for tag in todo.tags}
    assert tag_names == {"urgent", "work"}


@pytest.mark.asyncio
async def test_create_todo_with_invalid_tag_ids(async_session, test_user: User):
    """Test creating a todo with invalid tag IDs."""
    todo_service = TodoService(async_session)

    # Try to create todo with non-existent tag IDs
    todo_data = TodoCreate(
        title="Test todo",
        tag_ids=[uuid4(), uuid4()]  # Random UUIDs that don't exist
    )

    # Should create todo but without tags (invalid tags are ignored)
    todo = await todo_service.create_todo(test_user.id, todo_data)

    assert todo.id is not None
    assert len(todo.tags) == 0


@pytest.mark.asyncio
async def test_update_todo_add_tags(async_session, test_user: User):
    """Test adding tags to an existing todo."""
    # Create todo without tags
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(title="Test todo")
    todo = await todo_service.create_todo(test_user.id, todo_data)

    # Create tags
    tag_service = TagService(async_session)
    tag1 = await tag_service.create(TagCreate(name="personal"))
    tag2 = await tag_service.create(TagCreate(name="important"))

    # Update todo with tags
    update_data = TodoUpdate(tag_ids=[tag1.id, tag2.id])
    updated_todo = await todo_service.update_todo(todo.id, test_user.id, update_data)

    assert len(updated_todo.tags) == 2
    tag_names = {tag.name for tag in updated_todo.tags}
    assert tag_names == {"personal", "important"}


@pytest.mark.asyncio
async def test_update_todo_remove_tags(async_session, test_user: User):
    """Test removing tags from a todo."""
    # Create tags
    tag_service = TagService(async_session)
    tag1 = await tag_service.create(TagCreate(name="urgent"))
    tag2 = await tag_service.create(TagCreate(name="work"))

    # Create todo with tags
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo",
        tag_ids=[tag1.id, tag2.id]
    )
    todo = await todo_service.create_todo(test_user.id, todo_data)

    # Update todo to remove all tags
    update_data = TodoUpdate(tag_ids=[])
    updated_todo = await todo_service.update_todo(todo.id, test_user.id, update_data)

    assert len(updated_todo.tags) == 0


@pytest.mark.asyncio
async def test_update_todo_replace_tags(async_session, test_user: User):
    """Test replacing tags on a todo."""
    # Create tags
    tag_service = TagService(async_session)
    tag1 = await tag_service.create(TagCreate(name="urgent"))
    tag2 = await tag_service.create(TagCreate(name="work"))
    tag3 = await tag_service.create(TagCreate(name="personal"))

    # Create todo with first two tags
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo",
        tag_ids=[tag1.id, tag2.id]
    )
    todo = await todo_service.create_todo(test_user.id, todo_data)

    # Replace with different tag
    update_data = TodoUpdate(tag_ids=[tag3.id])
    updated_todo = await todo_service.update_todo(todo.id, test_user.id, update_data)

    assert len(updated_todo.tags) == 1
    assert updated_todo.tags[0].name == "personal"


@pytest.mark.asyncio
async def test_get_todos_includes_tags(async_session, test_user: User):
    """Test that getting todos includes their tags."""
    # Create tags
    tag_service = TagService(async_session)
    tag1 = await tag_service.create(TagCreate(name="urgent"))
    tag2 = await tag_service.create(TagCreate(name="work"))

    # Create todo with tags
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo with tags",
        tag_ids=[tag1.id, tag2.id]
    )
    await todo_service.create_todo(test_user.id, todo_data)

    # Get todos
    todos, _ = await todo_service.get_todos(test_user.id)

    assert len(todos) == 1
    assert len(todos[0].tags) == 2
    tag_names = {tag.name for tag in todos[0].tags}
    assert tag_names == {"urgent", "work"}


@pytest.mark.asyncio
async def test_get_todo_by_id_includes_tags(async_session, test_user: User):
    """Test that getting a single todo includes its tags."""
    # Create tag
    tag_service = TagService(async_session)
    tag = await tag_service.create(TagCreate(name="important"))

    # Create todo with tag
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo",
        tag_ids=[tag.id]
    )
    created_todo = await todo_service.create_todo(test_user.id, todo_data)

    # Get todo by ID
    todo = await todo_service.get_todo(created_todo.id, test_user.id)

    assert todo is not None
    assert len(todo.tags) == 1
    assert todo.tags[0].name == "important"


@pytest.mark.asyncio
async def test_delete_tag(async_session, test_user: User):
    """Test that a tag can be deleted."""
    # Create tag
    tag_service = TagService(async_session)
    tag = await tag_service.create(TagCreate(name="deletable"))

    # Verify it exists
    fetched_tag = await tag_service.get_by_id(tag.id)
    assert fetched_tag is not None
    assert fetched_tag.name == "deletable"

    # Delete the tag
    deleted = await tag_service.delete(tag.id)
    assert deleted is True
    
    # Verify it's gone
    deleted_tag = await tag_service.get_by_id(tag.id)
    assert deleted_tag is None


@pytest.mark.asyncio
async def test_todo_with_duplicate_tag_ids(async_session, test_user: User):
    """Test creating/updating todo with duplicate tag IDs."""
    # Create tag
    tag_service = TagService(async_session)
    tag = await tag_service.create(TagCreate(name="urgent"))

    # Create todo with duplicate tag IDs
    todo_service = TodoService(async_session)
    todo_data = TodoCreate(
        title="Test todo",
        tag_ids=[tag.id, tag.id, tag.id]  # Same tag ID multiple times
    )

    todo = await todo_service.create_todo(test_user.id, todo_data)

    # Should only have the tag once
    assert len(todo.tags) == 1
    assert todo.tags[0].name == "urgent"

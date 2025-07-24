"""Integration tests for todo endpoints with tag functionality."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.models.todo import Todo
from app.models.user import User


@pytest.mark.asyncio
async def test_create_todo_with_tags(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    async_session: AsyncSession
):
    """Test creating a todo with tags via API."""
    # Create tags first
    tag1 = Tag(name="urgent", color="#FF0000")
    tag2 = Tag(name="work", color="#0000FF")
    async_session.add_all([tag1, tag2])
    await async_session.commit()
    await async_session.refresh(tag1)
    await async_session.refresh(tag2)

    # Create todo with tags
    todo_data = {
        "title": "Todo with tags",
        "description": "This todo has multiple tags",
        "tag_ids": [str(tag1.id), str(tag2.id)]
    }

    response = await client.post(
        "/api/v1/todos/",
        json=todo_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 2
    tag_names = {tag["name"] for tag in data["tags"]}
    assert tag_names == {"urgent", "work"}


@pytest.mark.asyncio
async def test_update_todo_tags(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    async_session: AsyncSession
):
    """Test updating todo tags via API."""
    # Create tags
    tag1 = Tag(name="personal")
    tag2 = Tag(name="important")
    tag3 = Tag(name="work")
    async_session.add_all([tag1, tag2, tag3])
    await async_session.commit()
    await async_session.refresh(tag1)
    await async_session.refresh(tag2)
    await async_session.refresh(tag3)

    # Create todo with initial tags
    todo = Todo(
        title="Test todo",
        user_id=test_user.id,
        tags=[tag1, tag2]
    )
    async_session.add(todo)
    await async_session.commit()
    await async_session.refresh(todo)

    # Update todo to replace tags
    update_data = {
        "tag_ids": [str(tag2.id), str(tag3.id)]
    }

    response = await client.patch(
        f"/api/v1/todos/{todo.id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 2
    tag_names = {tag["name"] for tag in data["tags"]}
    assert tag_names == {"important", "work"}


@pytest.mark.asyncio
async def test_get_todos_with_tags(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    async_session: AsyncSession
):
    """Test getting todos includes their tags."""
    # Create tags
    tag1 = Tag(name="urgent")
    tag2 = Tag(name="personal")
    async_session.add_all([tag1, tag2])
    await async_session.commit()

    # Create todos with different tags
    todo1 = Todo(
        title="Work todo",
        user_id=test_user.id,
        tags=[tag1]
    )
    todo2 = Todo(
        title="Personal todo",
        user_id=test_user.id,
        tags=[tag2]
    )
    todo3 = Todo(
        title="Mixed todo",
        user_id=test_user.id,
        tags=[tag1, tag2]
    )
    async_session.add_all([todo1, todo2, todo3])
    await async_session.commit()

    # Get all todos
    response = await client.get(
        "/api/v1/todos/",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3

    # Verify each todo has correct tags
    todos_by_title = {todo["title"]: todo for todo in data["items"]}

    assert len(todos_by_title["Work todo"]["tags"]) == 1
    assert todos_by_title["Work todo"]["tags"][0]["name"] == "urgent"

    assert len(todos_by_title["Personal todo"]["tags"]) == 1
    assert todos_by_title["Personal todo"]["tags"][0]["name"] == "personal"

    assert len(todos_by_title["Mixed todo"]["tags"]) == 2
    mixed_tag_names = {tag["name"] for tag in todos_by_title["Mixed todo"]["tags"]}
    assert mixed_tag_names == {"urgent", "personal"}


@pytest.mark.asyncio
async def test_create_todo_with_invalid_tag_ids(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test creating todo with non-existent tag IDs."""
    todo_data = {
        "title": "Todo with invalid tags",
        "tag_ids": [
            "123e4567-e89b-12d3-a456-426614174000",
            "223e4567-e89b-12d3-a456-426614174000"
        ]
    }

    response = await client.post(
        "/api/v1/todos/",
        json=todo_data,
        headers=auth_headers
    )

    # Should still create the todo, just without tags
    assert response.status_code == 201
    data = response.json()
    assert len(data["tags"]) == 0


@pytest.mark.asyncio
async def test_remove_all_tags_from_todo(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    async_session: AsyncSession
):
    """Test removing all tags from a todo."""
    # Create tag
    tag = Tag(name="temporary")
    async_session.add(tag)
    await async_session.commit()

    # Create todo with tag
    todo = Todo(
        title="Todo with tag",
        user_id=test_user.id,
        tags=[tag]
    )
    async_session.add(todo)
    await async_session.commit()
    await async_session.refresh(todo)

    # Remove all tags
    update_data = {"tag_ids": []}

    response = await client.patch(
        f"/api/v1/todos/{todo.id}",
        json=update_data,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["tags"]) == 0


@pytest.mark.asyncio
async def test_tag_included_in_todo_response_fields(
    client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    async_session: AsyncSession
):
    """Test that tag response includes all expected fields."""
    # Create tag with all fields
    tag = Tag(name="detailed", color="#123456")
    async_session.add(tag)
    await async_session.commit()
    await async_session.refresh(tag)

    # Create todo with tag
    todo_data = {
        "title": "Test todo",
        "tag_ids": [str(tag.id)]
    }

    response = await client.post(
        "/api/v1/todos/",
        json=todo_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()

    # Check tag fields in response
    assert len(data["tags"]) == 1
    tag_data = data["tags"][0]
    assert "id" in tag_data
    assert tag_data["name"] == "detailed"
    assert tag_data["color"] == "#123456"
    assert "created_at" in tag_data
    assert "updated_at" in tag_data

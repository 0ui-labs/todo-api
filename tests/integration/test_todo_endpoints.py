from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Todo, User
from app.models.category import Category


@pytest.mark.asyncio
class TestTodoEndpoints:
    """Comprehensive tests for todo endpoints."""

    async def test_create_todo_minimal(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test creating todo with minimal data."""
        response = await client.post(
            "/api/v1/todos/",
            json={"title": "Simple Todo"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple Todo"
        assert data["status"] == "open"
        assert data["category_id"] is None

    async def test_create_todo_complete(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_category: Category
    ):
        """Test creating todo with all fields."""
        due_date = (datetime.now(UTC) + timedelta(days=7)).isoformat()
        response = await client.post(
            "/api/v1/todos/",
            json={
                "title": "Complete Todo",
                "description": "With all fields filled",
                "due_date": due_date,
                "category_id": str(test_category.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "With all fields filled"
        assert data["category_id"] == str(test_category.id)

    async def test_create_todo_with_category_eager_loaded(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_category: Category
    ):
        """Test creating todo returns eagerly loaded category."""
        response = await client.post(
            "/api/v1/todos/",
            json={
                "title": "Todo with Category",
                "category_id": str(test_category.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["category_id"] == str(test_category.id)
        # Verify category is eagerly loaded
        assert "category" in data
        assert data["category"]["id"] == str(test_category.id)
        assert data["category"]["name"] == test_category.name

    async def test_create_todo_invalid_category(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test creating todo with non-existent category."""
        response = await client.post(
            "/api/v1/todos/",
            json={
                "title": "Invalid Category Todo",
                "category_id": str(uuid4())
            },
            headers=auth_headers
        )
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    async def test_create_todo_with_other_users_category_fails(
        self,
        client: AsyncClient,
        auth_headers: dict,
        second_user_with_category: dict
    ):
        """Test that a user cannot create a todo with another user's category."""
        other_users_category_id = second_user_with_category["category"].id

        response = await client.post(
            "/api/v1/todos/",
            headers=auth_headers,
            json={
                "title": "Cross-User Todo Attempt",
                "category_id": str(other_users_category_id)
            }
        )

        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    async def test_list_todos(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_todos  # Fixture that creates multiple todos
    ):
        """Test listing todos with pagination."""
        response = await client.get(
            "/api/v1/todos/?offset=0&limit=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) <= 10
        assert "total" in data

    async def test_list_todos_filtered_by_completion(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_todos
    ):
        """Test filtering todos by completion status."""
        response = await client.get(
            "/api/v1/todos/?status=completed",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        todos = data["items"]
        assert all(todo["status"] == "completed" for todo in todos)

    async def test_search_todos(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_todos
    ):
        """Test searching todos by title/description."""
        response = await client.get(
            "/api/v1/todos/?search=important",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        todos = data["items"]
        for todo in todos:
            assert "important" in todo["title"].lower() or \
                   ("description" in todo and todo["description"] and
                    "important" in todo["description"].lower())

    async def test_list_todos_pagination_empty_page(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_todos
    ):
        """Test pagination with offset beyond available items."""
        response = await client.get(
            "/api/v1/todos/?offset=10&limit=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 3  # create_test_todos creates 3 todos

    async def test_list_todos_sorting_by_title_asc(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User,
        async_session: AsyncSession
    ):
        """Test sorting todos by title in ascending order."""
        # Create todos with specific titles
        todos = [
            Todo(
                user_id=test_user.id,
                title="C Task",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            ),
            Todo(
                user_id=test_user.id,
                title="A Task",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            ),
            Todo(
                user_id=test_user.id,
                title="B Task",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
        ]
        for todo in todos:
            async_session.add(todo)
        await async_session.commit()

        response = await client.get(
            "/api/v1/todos/?sort_by=title&order=asc",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        items = data["items"]
        assert len(items) == 3
        assert items[0]["title"] == "A Task"
        assert items[1]["title"] == "B Task"
        assert items[2]["title"] == "C Task"

    async def test_list_todos_sorting_by_due_date_desc(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User,
        async_session: AsyncSession
    ):
        """Test sorting todos by due date in descending order."""
        # Create todos with specific due dates
        now = datetime.now(UTC)
        todos = [
            Todo(
                user_id=test_user.id,
                title="Task 1",
                due_date=now + timedelta(days=1),
                created_at=now,
                updated_at=now
            ),
            Todo(
                user_id=test_user.id,
                title="Task 2",
                due_date=now + timedelta(days=2),
                created_at=now,
                updated_at=now
            ),
            Todo(
                user_id=test_user.id,
                title="Task 3",
                due_date=now + timedelta(days=3),
                created_at=now,
                updated_at=now
            )
        ]
        for todo in todos:
            async_session.add(todo)
        await async_session.commit()

        response = await client.get(
            "/api/v1/todos/?sort_by=due_date&order=desc",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        items = data["items"]
        assert len(items) == 3
        assert items[0]["title"] == "Task 3"  # Latest date first
        assert items[1]["title"] == "Task 2"
        assert items[2]["title"] == "Task 1"

    async def test_get_todo_by_id(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_todo: Todo
    ):
        """Test getting a specific todo."""
        response = await client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_todo.id)
        assert data["title"] == test_todo.title

    async def test_get_todo_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting non-existent todo."""
        response = await client.get(
            f"/api/v1/todos/{uuid4()}",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_get_todo_wrong_user(
        self,
        client: AsyncClient,
        other_user_todo: Todo,
        auth_headers: dict
    ):
        """Test accessing another user's todo."""
        response = await client.get(
            f"/api/v1/todos/{other_user_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 404  # Should appear as not found

    async def test_update_todo(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_todo: Todo
    ):
        """Test updating a todo."""
        response = await client.patch(
            f"/api/v1/todos/{test_todo.id}",
            json={
                "title": "Updated Title",
                "status": "completed"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "completed"

    async def test_update_todo_partial(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_todo: Todo
    ):
        """Test partial update (only some fields)."""
        response = await client.patch(
            f"/api/v1/todos/{test_todo.id}",
            json={"title": test_todo.title, "status": "completed"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["title"] == test_todo.title  # Unchanged

    async def test_delete_todo(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_todo: Todo
    ):
        """Test deleting a todo."""
        response = await client.delete(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert response.status_code == 204

        # Verify it's deleted
        get_response = await client.get(
            f"/api/v1/todos/{test_todo.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_soft_deleted_todo_is_hidden_from_list_and_get(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User,
        async_session: AsyncSession
    ):
        """Test that soft-deleted todos are hidden from list and get endpoints."""
        # Create 3 todos
        todos = []
        for i in range(3):
            todo = Todo(
                user_id=test_user.id,
                title=f"Todo {i+1}",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )
            async_session.add(todo)
            todos.append(todo)
        await async_session.commit()

        # Get initial count
        response = await client.get("/api/v1/todos/", headers=auth_headers)
        assert response.status_code == 200
        initial_data = response.json()
        initial_total = initial_data["total"]

        # Delete one todo
        todo_to_delete_id = todos[1].id
        delete_response = await client.delete(
            f"/api/v1/todos/{todo_to_delete_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == 204

        # Check list endpoint - deleted todo should not be visible
        list_response = await client.get("/api/v1/todos/", headers=auth_headers)
        assert list_response.status_code == 200
        list_data = list_response.json()

        # Verify total count is reduced
        assert list_data["total"] == initial_total - 1

        # Verify deleted todo is not in the list
        todo_ids = [todo["id"] for todo in list_data["items"]]
        assert str(todo_to_delete_id) not in todo_ids

        # Check get endpoint - should return 404
        get_response = await client.get(
            f"/api/v1/todos/{todo_to_delete_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    @pytest.mark.skip(reason="Bulk update endpoint not implemented")
    async def test_bulk_update_todos(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_todos
    ):
        """Test bulk updating multiple todos."""
        # Get todo IDs
        list_response = await client.get(
            "/api/v1/todos/",
            headers=auth_headers
        )
        data = list_response.json()
        assert "items" in data
        todos = data["items"]
        todo_ids = [todo["id"] for todo in todos[:3]]

        # Bulk update
        response = await client.patch(
            "/api/v1/todos/bulk",
            json={
                "todo_ids": todo_ids,
                "updates": {"status": "completed"}
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["updated"] == len(todo_ids)

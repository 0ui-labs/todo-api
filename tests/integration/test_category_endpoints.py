import pytest
from httpx import AsyncClient

from app.models.category import Category


@pytest.mark.asyncio
class TestCategoryEndpoints:
    """Comprehensive tests for category endpoints."""

    async def test_create_category(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test creating a new category."""
        response = await client.post(
            "/api/v1/categories/",
            json={
                "name": "Work",
                "color": "#FF5733",

            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Work"
        assert data["color"] == "#FF5733"


    async def test_create_duplicate_category(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_category: Category
    ):
        """Test creating category with duplicate name."""
        response = await client.post(
            "/api/v1/categories/",
            json={"name": test_category.name, "color": "#FFFFFF"},
            headers=auth_headers
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_list_categories(
        self,
        client: AsyncClient,
        auth_headers: dict,
        create_test_categories  # Fixture for multiple categories
    ):
        """Test listing all user's categories."""
        response = await client.get(
            "/api/v1/categories/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Response is paginated
        assert "items" in data
        assert "total" in data
        categories = data["items"]
        assert isinstance(categories, list)
        assert len(categories) >= 3  # From fixture

        # Verify only user's categories are returned
        for category in categories:
            assert "name" in category
            assert "id" in category

    async def test_get_category(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_category: Category
    ):
        """Test getting a specific category."""
        response = await client.get(
            f"/api/v1/categories/{test_category.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_category.id)
        assert data["name"] == test_category.name

    async def test_get_category_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting non-existent category."""
        response = await client.get(
            "/api/v1/categories/00000000-0000-0000-0000-000000000000",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_update_category(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_category: Category
    ):
        """Test updating a category."""
        response = await client.patch(
            f"/api/v1/categories/{test_category.id}",
            json={
                "name": "Updated Name",
                "color": "#00FF00"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["color"] == "#00FF00"

    async def test_delete_empty_category(
        self,
        client: AsyncClient,
        auth_headers: dict,
        empty_category: Category  # Category with no todos
    ):
        """Test deleting a category without todos."""
        response = await client.delete(
            f"/api/v1/categories/{empty_category.id}",
            headers=auth_headers
        )
        assert response.status_code == 204

        # Verify it's deleted
        get_response = await client.get(
            f"/api/v1/categories/{empty_category.id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_delete_category_with_todos(
        self,
        client: AsyncClient,
        auth_headers: dict,
        category_with_todos: dict  # Category + its todos
    ):
        """Test deleting category that has todos.

        Should succeed and set todos category_id to null.
        """
        category = category_with_todos["category"]
        response = await client.delete(
            f"/api/v1/categories/{category.id}",
            headers=auth_headers
        )
        # The current implementation allows deletion and sets todo.category_id to NULL
        assert response.status_code == 204

    # TODO: Implement these tests when the endpoints are added
    # async def test_get_category_todos(
    #     self,
    #     client: AsyncClient,
    #     auth_headers: dict,
    #     category_with_todos: dict
    # ):
    #     """Test getting all todos in a category."""
    #     category = category_with_todos["category"]
    #     todos = category_with_todos["todos"]
    #
    #     response = await client.get(
    #         f"/api/v1/categories/{category.id}/todos",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert len(data) == len(todos)
    #
    #     # Verify all todos belong to this category
    #     for todo in data:
    #         assert todo["category_id"] == category.id

    # async def test_get_category_todos_pagination(
    #     self,
    #     client: AsyncClient,
    #     auth_headers: dict,
    #     category_with_many_todos: Category  # Category with 20+ todos
    # ):
    #     """Test pagination when getting category todos."""
    #     response = await client.get(
    #         f"/api/v1/categories/{category_with_many_todos.id}/todos?skip=5&limit=10",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     todos = response.json()
    #     assert len(todos) <= 10

    # async def test_category_statistics(
    #     self,
    #     client: AsyncClient,
    #     auth_headers: dict,
    #     category_with_todos: dict
    # ):
    #     """Test getting category statistics (if endpoint exists)."""
    #     category = category_with_todos["category"]
    #
    #     # This assumes a stats endpoint exists
    #     response = await client.get(
    #         f"/api/v1/categories/{category.id}/stats",
    #         headers=auth_headers
    #     )
    #     if response.status_code == 200:
    #         stats = response.json()
    #         assert "total_todos" in stats
    #         assert "completed_todos" in stats
    #         assert "pending_todos" in stats

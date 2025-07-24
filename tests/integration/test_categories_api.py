"""Integration tests for categories API endpoints."""
from uuid import uuid4

import pytest
from httpx import AsyncClient

from app.models.category import Category
from app.models.user import User

pytestmark = pytest.mark.asyncio


class TestCategoriesAPI:
    """Test categories API endpoints."""

    async def test_create_category_success(
        self, client: AsyncClient, test_user: User, auth_headers: dict
    ) -> None:
        """Test successful category creation."""
        payload = {
            "name": "Work",
            "color": "#FF5733"
        }

        response = await client.post(
            "/api/v1/categories/",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["color"] == payload["color"]
        assert data["user_id"] == str(test_user.id)
        assert "id" in data
        assert "created_at" in data

    async def test_create_category_duplicate_name(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test creating category with duplicate name."""
        # Create first category
        category = Category(
            user_id=test_user.id,
            name="Existing Category",
            color="#000000"
        )
        test_db.add(category)
        await test_db.commit()

        # Try to create duplicate
        payload = {
            "name": "Existing Category",
            "color": "#FF5733"
        }

        response = await client.post(
            "/api/v1/categories/",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_create_category_unauthorized(
        self, client: AsyncClient
    ) -> None:
        """Test creating category without authentication."""
        payload = {
            "name": "Work",
            "color": "#FF5733"
        }

        response = await client.post(
            "/api/v1/categories/",
            json=payload
        )

        assert response.status_code == 403

    async def test_get_categories_empty(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        """Test getting categories when none exist."""
        response = await client.get(
            "/api/v1/categories/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["limit"] == 20
        assert data["offset"] == 0

    async def test_get_categories_with_data(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test getting categories with existing data."""
        # Create test categories
        categories = [
            Category(user_id=test_user.id, name="Work", color="#FF0000"),
            Category(user_id=test_user.id, name="Personal", color="#00FF00"),
            Category(user_id=test_user.id, name="Shopping", color="#0000FF"),
        ]
        for cat in categories:
            test_db.add(cat)
        await test_db.commit()

        response = await client.get(
            "/api/v1/categories/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

        # Check that only user's categories are returned
        for item in data["items"]:
            assert item["user_id"] == str(test_user.id)

    async def test_get_categories_with_search(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test searching categories."""
        # Create test categories
        categories = [
            Category(user_id=test_user.id, name="Work Tasks", color="#FF0000"),
            Category(user_id=test_user.id, name="Personal", color="#00FF00"),
            Category(user_id=test_user.id, name="Work Projects", color="#0000FF"),
        ]
        for cat in categories:
            test_db.add(cat)
        await test_db.commit()

        response = await client.get(
            "/api/v1/categories?search=work",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert all("Work" in item["name"] for item in data["items"])

    async def test_get_categories_with_pagination(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test categories pagination."""
        # Create test categories
        for i in range(5):
            category = Category(
                user_id=test_user.id,
                name=f"Category {i}",
                color="#000000"
            )
            test_db.add(category)
        await test_db.commit()

        # Get first page
        response = await client.get(
            "/api/v1/categories?limit=2&offset=0",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["limit"] == 2
        assert data["offset"] == 0

        # Get second page
        response = await client.get(
            "/api/v1/categories?limit=2&offset=2",
            headers=auth_headers
        )

        data = response.json()
        assert len(data["items"]) == 2
        assert data["offset"] == 2

    async def test_get_category_by_id(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test getting a specific category."""
        # Create test category
        category = Category(
            user_id=test_user.id,
            name="Test Category",
            color="#FF5733"
        )
        test_db.add(category)
        await test_db.commit()
        await test_db.refresh(category)

        response = await client.get(
            f"/api/v1/categories/{category.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(category.id)
        assert data["name"] == category.name
        assert data["color"] == category.color

    async def test_get_category_not_found(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        """Test getting non-existent category."""
        fake_id = uuid4()

        response = await client.get(
            f"/api/v1/categories/{fake_id}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    async def test_get_category_from_other_user(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test that users cannot access other users' categories."""
        # Create another user's category
        other_user_id = uuid4()
        category = Category(
            user_id=other_user_id,
            name="Other User Category",
            color="#000000"
        )
        test_db.add(category)
        await test_db.commit()
        await test_db.refresh(category)

        response = await client.get(
            f"/api/v1/categories/{category.id}",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_update_category_success(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test successful category update."""
        # Create test category
        category = Category(
            user_id=test_user.id,
            name="Old Name",
            color="#000000"
        )
        test_db.add(category)
        await test_db.commit()
        await test_db.refresh(category)

        payload = {
            "name": "New Name",
            "color": "#FF5733"
        }

        response = await client.patch(
            f"/api/v1/categories/{category.id}",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["color"] == payload["color"]

    async def test_update_category_partial(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test partial category update."""
        # Create test category
        category = Category(
            user_id=test_user.id,
            name="Original Name",
            color="#000000"
        )
        test_db.add(category)
        await test_db.commit()
        await test_db.refresh(category)

        # Update only name
        payload = {"name": "Updated Name"}

        response = await client.patch(
            f"/api/v1/categories/{category.id}",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["color"] == category.color  # Color unchanged

    async def test_update_category_duplicate_name(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test updating category to duplicate name."""
        # Create two categories
        category1 = Category(user_id=test_user.id, name="Category 1", color="#000000")
        category2 = Category(user_id=test_user.id, name="Category 2", color="#FFFFFF")
        test_db.add(category1)
        test_db.add(category2)
        await test_db.commit()
        await test_db.refresh(category2)

        # Try to rename category2 to category1's name
        payload = {"name": "Category 1"}

        response = await client.patch(
            f"/api/v1/categories/{category2.id}",
            json=payload,
            headers=auth_headers
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_delete_category_success(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test successful category deletion."""
        # Create test category
        category = Category(
            user_id=test_user.id,
            name="To Delete",
            color="#FF0000"
        )
        test_db.add(category)
        await test_db.commit()
        await test_db.refresh(category)

        response = await client.delete(
            f"/api/v1/categories/{category.id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # Verify it's deleted
        response = await client.get(
            f"/api/v1/categories/{category.id}",
            headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_category_not_found(
        self, client: AsyncClient, auth_headers: dict
    ) -> None:
        """Test deleting non-existent category."""
        fake_id = uuid4()

        response = await client.delete(
            f"/api/v1/categories/{fake_id}",
            headers=auth_headers
        )

        assert response.status_code == 404

    async def test_category_isolation_between_users(
        self, client: AsyncClient, test_user: User, auth_headers: dict, test_db
    ) -> None:
        """Test that categories are properly isolated between users."""
        # Create categories for different users
        user1_id = test_user.id
        user2_id = uuid4()

        categories = [
            Category(user_id=user1_id, name="User1 Category", color="#FF0000"),
            Category(user_id=user2_id, name="User2 Category", color="#00FF00"),
        ]
        for cat in categories:
            test_db.add(cat)
        await test_db.commit()

        # Get categories for authenticated user
        response = await client.get(
            "/api/v1/categories/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "User1 Category"

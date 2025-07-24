"""Simple integration tests for categories API without database user creation."""
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user_id
from app.main import app

pytestmark = pytest.mark.asyncio


@pytest.fixture
def test_user_id() -> None:
    """Return a test user ID."""
    return str(uuid4())


@pytest_asyncio.fixture
async def client_with_auth(
    test_user_id: str, client: AsyncClient, async_session: AsyncSession
):
    """Create a test client with mocked authentication."""
    async def mock_get_current_user_id():
        return test_user_id

    app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

    yield client

    # Clear only the auth override, keep the db override
    del app.dependency_overrides[get_current_user_id]


class TestCategoriesAPISimple:
    """Simple test categories API endpoints."""

    async def test_create_and_get_category(self, client_with_auth: AsyncClient) -> None:
        """Test creating and retrieving a category."""
        # Create category
        payload = {
            "name": "Work",
            "color": "#FF5733"
        }

        response = await client_with_auth.post(
            "/api/v1/categories/",
            json=payload
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["color"] == payload["color"]
        assert "id" in data
        category_id = data["id"]

        # Get the category
        response = await client_with_auth.get(
            f"/api/v1/categories/{category_id}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == payload["name"]

    async def test_list_categories(self, client_with_auth: AsyncClient) -> None:
        """Test listing categories with pagination."""
        # Create multiple categories
        for i in range(3):
            payload = {
                "name": f"Category {i}",
                "color": "#000000"
            }
            response = await client_with_auth.post(
                "/api/v1/categories/",
                json=payload
            )
            assert response.status_code == 201

        # List categories
        response = await client_with_auth.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    async def test_update_category(self, client_with_auth: AsyncClient) -> None:
        """Test updating a category."""
        # Create category
        create_payload = {
            "name": "Original",
            "color": "#FF0000"
        }
        response = await client_with_auth.post(
            "/api/v1/categories/",
            json=create_payload
        )
        assert response.status_code == 201
        category_id = response.json()["id"]

        # Update category
        update_payload = {
            "name": "Updated",
            "color": "#00FF00"
        }
        response = await client_with_auth.patch(
            f"/api/v1/categories/{category_id}",
            json=update_payload
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_payload["name"]
        assert data["color"] == update_payload["color"]

    async def test_delete_category(self, client_with_auth: AsyncClient) -> None:
        """Test deleting a category."""
        # Create category
        payload = {
            "name": "To Delete",
            "color": "#FF0000"
        }
        response = await client_with_auth.post(
            "/api/v1/categories/",
            json=payload
        )
        assert response.status_code == 201
        category_id = response.json()["id"]

        # Delete category
        response = await client_with_auth.delete(
            f"/api/v1/categories/{category_id}"
        )
        assert response.status_code == 204

        # Verify it's deleted
        response = await client_with_auth.get(
            f"/api/v1/categories/{category_id}"
        )
        assert response.status_code == 404

    async def test_authorization_required(self) -> None:
        """Test that endpoints require authentication."""
        from httpx import ASGITransport
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Test without auth
            response = await client.get("/api/v1/categories/")
            assert response.status_code == 403

            response = await client.post(
                "/api/v1/categories/",
                json={"name": "Test", "color": "#000000"}
            )
            assert response.status_code == 403

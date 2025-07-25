"""Integration test for complete categories workflow - from test_categories_curl.sh."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCategoriesWorkflow:
    """Test full end-to-end workflow for categories API."""

    async def test_full_category_workflow(
        self, client: AsyncClient, auth_headers: dict
    ):
        """Test complete workflow: CRUD operations on categories.

        Note: This test uses existing test user fixture instead of creating
        a new user to avoid Redis connectivity issues in test environment.
        """
        # Step 1: Create category (Work)
        create_payload = {"name": "Work", "color": "#FF5733"}
        response = await client.post(
            "/api/v1/categories/", json=create_payload, headers=auth_headers
        )
        assert response.status_code == 201
        work_category = response.json()
        category_id = work_category["id"]
        assert work_category["name"] == "Work"
        assert work_category["color"] == "#FF5733"

        # Step 2: Create another category (Personal)
        create_payload = {"name": "Personal", "color": "#00FF00"}
        response = await client.post(
            "/api/v1/categories/", json=create_payload, headers=auth_headers
        )
        assert response.status_code == 201
        personal_category = response.json()
        assert personal_category["name"] == "Personal"
        assert personal_category["color"] == "#00FF00"

        # Step 3: List all categories
        response = await client.get("/api/v1/categories/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        category_names = [cat["name"] for cat in data["items"]]
        assert "Work" in category_names
        assert "Personal" in category_names

        # Step 4: Get specific category
        response = await client.get(
            f"/api/v1/categories/{category_id}", headers=auth_headers
        )
        assert response.status_code == 200
        category = response.json()
        assert category["id"] == category_id
        assert category["name"] == "Work"
        assert category["color"] == "#FF5733"

        # Step 5: Update category
        update_payload = {"name": "Work Projects", "color": "#0000FF"}
        response = await client.patch(
            f"/api/v1/categories/{category_id}",
            json=update_payload,
            headers=auth_headers
        )
        assert response.status_code == 200
        updated_category = response.json()
        assert updated_category["name"] == "Work Projects"
        assert updated_category["color"] == "#0000FF"

        # Step 6: Search categories
        response = await client.get(
            "/api/v1/categories/?search=project", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Work Projects"

        # Step 7: Test pagination
        response = await client.get(
            "/api/v1/categories/?limit=1&offset=0", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 1
        assert data["limit"] == 1
        assert data["offset"] == 0

        # Second page
        response = await client.get(
            "/api/v1/categories/?limit=1&offset=1", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 1
        assert data["offset"] == 1

        # Step 8: Delete category
        response = await client.delete(
            f"/api/v1/categories/{category_id}", headers=auth_headers
        )
        assert response.status_code == 204

        # Step 9: Verify category is deleted
        response = await client.get(
            f"/api/v1/categories/{category_id}", headers=auth_headers
        )
        assert response.status_code == 404

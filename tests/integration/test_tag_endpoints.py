"""Integration tests for tag endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.models.user import User
from app.schemas.tag import TagCreate


@pytest.mark.asyncio
async def test_create_tag(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test creating a new tag."""
    tag_data = {
        "name": "urgent",
        "color": "#FF0000"
    }
    
    response = await test_client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "urgent"
    assert data["color"] == "#FF0000"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_tag_duplicate_name(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test creating a tag with duplicate name fails."""
    # Create first tag
    tag = Tag(name="urgent", color="#FF0000")
    db_session.add(tag)
    await db_session.commit()
    
    # Try to create duplicate
    tag_data = {"name": "urgent", "color": "#00FF00"}
    
    response = await test_client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_tag_invalid_color(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test creating a tag with invalid color format."""
    tag_data = {
        "name": "test",
        "color": "red"  # Invalid format
    }
    
    response = await test_client.post(
        "/api/v1/tags/",
        json=tag_data,
        headers=auth_headers
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_tags(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test getting all tags."""
    # Create test tags
    tags = [
        Tag(name="urgent", color="#FF0000"),
        Tag(name="work", color="#0000FF"),
        Tag(name="personal", color="#00FF00"),
    ]
    db_session.add_all(tags)
    await db_session.commit()
    
    response = await test_client.get(
        "/api/v1/tags/",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Should be ordered by name
    assert data[0]["name"] == "personal"
    assert data[1]["name"] == "urgent"
    assert data[2]["name"] == "work"


@pytest.mark.asyncio
async def test_get_tag_by_id(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test getting a specific tag."""
    # Create tag
    tag = Tag(name="important", color="#FF00FF")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    
    response = await test_client.get(
        f"/api/v1/tags/{tag.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(tag.id)
    assert data["name"] == "important"
    assert data["color"] == "#FF00FF"


@pytest.mark.asyncio
async def test_get_tag_not_found(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test getting a non-existent tag."""
    response = await test_client.get(
        "/api/v1/tags/123e4567-e89b-12d3-a456-426614174000",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_tag(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test updating a tag."""
    # Create tag
    tag = Tag(name="urgent", color="#FF0000")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    
    update_data = {
        "name": "very urgent",
        "color": "#FF5500"
    }
    
    response = await test_client.put(
        f"/api/v1/tags/{tag.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "very urgent"
    assert data["color"] == "#FF5500"


@pytest.mark.asyncio
async def test_update_tag_partial(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test partial update of a tag."""
    # Create tag
    tag = Tag(name="work", color="#0000FF")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    
    # Update only color
    update_data = {"color": "#00FF00"}
    
    response = await test_client.put(
        f"/api/v1/tags/{tag.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "work"  # Unchanged
    assert data["color"] == "#00FF00"  # Updated


@pytest.mark.asyncio
async def test_update_tag_duplicate_name(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test updating a tag to duplicate name fails."""
    # Create two tags
    tag1 = Tag(name="urgent")
    tag2 = Tag(name="work")
    db_session.add_all([tag1, tag2])
    await db_session.commit()
    await db_session.refresh(tag2)
    
    # Try to update tag2 with tag1's name
    update_data = {"name": "urgent"}
    
    response = await test_client.put(
        f"/api/v1/tags/{tag2.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_tag(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict,
    db_session: AsyncSession
):
    """Test deleting a tag."""
    # Create tag
    tag = Tag(name="temporary")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    
    response = await test_client.delete(
        f"/api/v1/tags/{tag.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = await test_client.get(
        f"/api/v1/tags/{tag.id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_tag_not_found(
    test_client: AsyncClient,
    test_user: User,
    auth_headers: dict
):
    """Test deleting a non-existent tag."""
    response = await test_client.delete(
        "/api/v1/tags/123e4567-e89b-12d3-a456-426614174000",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_tag_endpoints_require_auth(test_client: AsyncClient):
    """Test that all tag endpoints require authentication."""
    tag_id = "123e4567-e89b-12d3-a456-426614174000"
    
    # Test all endpoints without auth
    endpoints = [
        ("POST", "/api/v1/tags/", {"name": "test"}),
        ("GET", "/api/v1/tags/", None),
        ("GET", f"/api/v1/tags/{tag_id}", None),
        ("PUT", f"/api/v1/tags/{tag_id}", {"name": "test"}),
        ("DELETE", f"/api/v1/tags/{tag_id}", None),
    ]
    
    for method, url, json_data in endpoints:
        if method == "POST":
            response = await test_client.post(url, json=json_data)
        elif method == "GET":
            response = await test_client.get(url)
        elif method == "PUT":
            response = await test_client.put(url, json=json_data)
        elif method == "DELETE":
            response = await test_client.delete(url)
        
        assert response.status_code == 401, f"{method} {url} should require auth"
"""Test request size limit middleware."""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_request_size_limit_small_payload(test_user_headers):
    """Test that small payloads are accepted."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a small payload (less than 10MB)
        small_data = {"title": "Test Todo", "description": "A" * 1000}
        
        response = await client.post(
            "/api/v1/todos",
            json=small_data,
            headers=test_user_headers
        )
        
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_request_size_limit_large_payload(test_user_headers):
    """Test that large payloads are rejected with 413 status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a large payload (more than 10MB)
        # 11MB of data
        large_description = "A" * (11 * 1024 * 1024)
        large_data = {"title": "Test Todo", "description": large_description}
        
        # Manually set content-length header to simulate large request
        headers = {
            **test_user_headers,
            "Content-Length": str(11 * 1024 * 1024)
        }
        
        response = await client.post(
            "/api/v1/todos",
            json=large_data,
            headers=headers
        )
        
        assert response.status_code == 413
        assert response.json()["detail"] == "Request too large"


@pytest.mark.asyncio
async def test_request_size_limit_exact_10mb():
    """Test that exactly 10MB payload is accepted."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with exactly 10MB content-length header
        headers = {
            "Content-Length": str(10 * 1024 * 1024)
        }
        
        response = await client.get(
            "/health",
            headers=headers
        )
        
        # Should not reject as it's exactly at the limit
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_request_size_limit_just_over_10mb():
    """Test that payload just over 10MB is rejected."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with just over 10MB
        headers = {
            "Content-Length": str(10 * 1024 * 1024 + 1)
        }
        
        response = await client.get(
            "/health",
            headers=headers
        )
        
        assert response.status_code == 413
        assert response.json()["detail"] == "Request too large"


@pytest.mark.asyncio
async def test_request_size_limit_no_content_length():
    """Test that requests without content-length header are allowed."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Request without content-length header should be allowed
        response = await client.get("/health")
        
        assert response.status_code == 200
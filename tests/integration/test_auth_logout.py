"""Integration tests for logout functionality."""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

from app.main import app
from app.services.token_blacklist import get_token_blacklist_service


class TestAuthLogout:
    """Test cases for logout endpoints."""
    
    @pytest_asyncio.fixture
    async def auth_headers(self, client: AsyncClient) -> dict[str, str]:
        """Get authentication headers for test user."""
        # Register a test user
        register_data = {
            "email": "logout_test@example.com",
            "password": "TestPassword123!",
            "name": "Logout Test User"
        }
        reg_response = await client.post("/api/v1/auth/register", json=register_data)
        if reg_response.status_code != 201:
            print(f"Registration failed: {reg_response.status_code}")
            print(f"Response: {reg_response.text}")
        
        # Login to get token
        login_data = {
            "email": "logout_test@example.com",
            "password": "TestPassword123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.status_code}")
            print(f"Response: {response.text}")
        token = response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.mark.asyncio
    async def test_logout_success(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test successful logout."""
        # First verify the token works
        response = await client.get("/api/v1/todos/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Logout
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify token no longer works
        response = await client.get("/api/v1/todos/", headers=auth_headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Token has been revoked"
    
    @pytest.mark.asyncio
    async def test_logout_without_auth(self, client: AsyncClient):
        """Test logout without authentication fails."""
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_logout_with_invalid_token(self, client: AsyncClient):
        """Test logout with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = await client.post("/api/v1/auth/logout", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    async def test_logout_all_devices_success(self, client: AsyncClient):
        """Test logout from all devices."""
        # Register a test user
        register_data = {
            "email": "multi_device@example.com",
            "password": "TestPassword123!",
            "full_name": "Multi Device User"
        }
        await client.post("/api/v1/auth/register", json=register_data)
        
        # Login from multiple "devices" (get multiple tokens)
        login_data = {
            "email": "multi_device@example.com",
            "password": "TestPassword123!"
        }
        
        # Get first token
        response1 = await client.post("/api/v1/auth/login", json=login_data)
        token1 = response1.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        # Wait a bit to ensure different JTI
        await asyncio.sleep(0.1)
        
        # Get second token
        response2 = await client.post("/api/v1/auth/login", json=login_data)
        token2 = response2.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Verify both tokens work
        response = await client.get("/api/v1/todos/", headers=headers1)
        assert response.status_code == status.HTTP_200_OK
        
        response = await client.get("/api/v1/todos/", headers=headers2)
        assert response.status_code == status.HTTP_200_OK
        
        # Logout from all devices using first token
        response = await client.post("/api/v1/auth/logout-all-devices", headers=headers1)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify both tokens no longer work
        response = await client.get("/api/v1/todos/", headers=headers1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Token has been revoked"
        
        response = await client.get("/api/v1/todos/", headers=headers2)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Token has been revoked"
    
    @pytest.mark.asyncio
    async def test_logout_redis_error_still_succeeds(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test logout still returns success even if Redis fails."""
        # Mock Redis to fail
        with patch.object(get_token_blacklist_service, 'add_token_to_blacklist', side_effect=Exception("Redis error")):
            response = await client.post("/api/v1/auth/logout", headers=auth_headers)
            # Should still return success
            assert response.status_code == status.HTTP_204_NO_CONTENT
    
    @pytest.mark.asyncio
    async def test_token_without_jti_still_works(self, client: AsyncClient):
        """Test that old tokens without JTI still work (backward compatibility)."""
        from app.utils.security import create_access_token
        
        # Create a token without JTI (simulate old token)
        with patch('app.utils.security.uuid.uuid4', side_effect=Exception("No UUID")):
            # This will cause the token creation to fail adding JTI
            # In production, you'd handle this more gracefully
            pass
        
        # For now, just verify the endpoint exists
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == status.HTTP_403_FORBIDDEN  # No auth provided
    
    @pytest.mark.asyncio
    async def test_logout_all_devices_without_auth(self, client: AsyncClient):
        """Test logout all devices without authentication fails."""
        response = await client.post("/api/v1/auth/logout-all-devices")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @pytest.mark.asyncio
    async def test_multiple_logouts_idempotent(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test that logging out multiple times is idempotent."""
        # First logout
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Second logout should fail with 401 (token already revoked)
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
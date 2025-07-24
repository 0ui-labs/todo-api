"""Simplified integration tests for logout functionality with mocked Redis."""

from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


class TestAuthLogoutSimple:
    """Simplified test cases for logout endpoints."""

    @pytest_asyncio.fixture(autouse=True)
    async def mock_redis(self):
        """Mock Redis for all tests."""
        # Create a mock Redis client
        mock_redis_client = AsyncMock()
        mock_redis_client.setex = AsyncMock(return_value=True)
        mock_redis_client.exists = AsyncMock(return_value=0)
        mock_redis_client.get = AsyncMock(return_value=None)
        mock_redis_client.incr = AsyncMock(return_value=1)
        mock_redis_client.expire = AsyncMock(return_value=True)

        # Create async function that returns the mock
        async def mock_from_url(*args, **kwargs):
            return mock_redis_client

        # Patch the Redis connection
        with patch(
            'app.services.token_blacklist.redis.from_url',
            side_effect=mock_from_url
        ):
            # Also patch the global service instance to ensure fresh state
            with patch('app.services.token_blacklist._blacklist_service', None):
                yield mock_redis_client

    @pytest_asyncio.fixture
    async def auth_headers(self, client: AsyncClient) -> dict[str, str]:
        """Get authentication headers for test user."""
        # Register a test user
        register_data = {
            "email": "logout_test_simple@example.com",
            "password": "TestPassword123!",
            "name": "Logout Test User"
        }
        await client.post("/api/v1/auth/register", json=register_data)

        # Login to get token
        login_data = {
            "email": "logout_test_simple@example.com",
            "password": "TestPassword123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        token = response.json()["access_token"]

        return {"Authorization": f"Bearer {token}"}

    @pytest.mark.asyncio
    async def test_logout_basic(
        self, client: AsyncClient,
        auth_headers: dict[str, str],
        mock_redis
    ):
        """Test basic logout functionality."""
        # Logout
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify token was added to blacklist
        assert mock_redis.setex.called
        call_args = mock_redis.setex.call_args
        assert "token_blacklist:" in call_args[0][0]  # Check key format

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
    async def test_logout_all_devices(
        self, client: AsyncClient,
        auth_headers: dict[str, str],
        mock_redis
    ):
        """Test logout from all devices."""
        # Logout from all devices
        response = await client.post(
            "/api/v1/auth/logout-all-devices", headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify user token version was incremented
        assert mock_redis.incr.called
        call_args = mock_redis.incr.call_args
        assert "user_token_version:" in call_args[0][0]  # Check key format

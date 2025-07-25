"""Integration tests for token revocation functionality."""

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from jose import jwt

from app.config import settings


class TestTokenRevocation:
    """Test cases for token revocation with race condition fixes."""

    @pytest_asyncio.fixture
    async def test_user_credentials(self):
        """Test user credentials."""
        return {
            "email": "revoke_test@example.com",
            "password": "TestPassword123!",
            "name": "Revoke Test User"
        }

    @pytest_asyncio.fixture
    async def authenticated_client(self, client: AsyncClient, test_user_credentials) -> tuple[AsyncClient, str, dict]:
        """Get authenticated client with token."""
        # Register user
        reg_response = await client.post("/api/v1/auth/register", json=test_user_credentials)
        assert reg_response.status_code == 201

        # Login to get token
        login_data = {
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        }
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        return client, token, headers

    @pytest.mark.asyncio
    async def test_token_revocation_immediate_effect(self, authenticated_client):
        """
        Verify that token revocation takes immediate effect.
        
        1. User logs in and receives token
        2. User logs out (increments token version)
        3. Old token immediately becomes invalid
        """
        client, token, headers = authenticated_client

        # Verify token works before logout
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK

        # Decode token to check version
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
        initial_version = payload.get("token_version", 0)

        # Logout (this should increment token version)
        logout_response = await client.post("/api/v1/auth/logout", headers=headers)
        assert logout_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify token is immediately invalid
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Token has been revoked"

    @pytest.mark.asyncio
    async def test_token_version_persists_across_requests(self, authenticated_client):
        """Verify token version is consistent across async contexts."""
        client, token, headers = authenticated_client

        # Decode token to get version
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
        token_version = payload.get("token_version", 0)

        # Make multiple concurrent requests
        import asyncio

        async def make_request():
            response = await client.get("/api/v1/todos/", headers=headers)
            return response.status_code

        # Run 10 concurrent requests
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should succeed with same token
        assert all(status_code == status.HTTP_200_OK for status_code in results)

        # Logout
        await client.post("/api/v1/auth/logout", headers=headers)

        # Run 10 more concurrent requests
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All should fail with 401
        assert all(
            status_code == status.HTTP_401_UNAUTHORIZED
            for status_code in results
            if not isinstance(status_code, Exception)
        )

    @pytest.mark.asyncio
    async def test_new_login_after_logout_gets_new_version(self, client: AsyncClient, test_user_credentials):
        """Verify that logging in after logout gets a new token with updated version."""
        # First login
        login_data = {
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        }

        # Register first
        await client.post("/api/v1/auth/register", json=test_user_credentials)

        # Login
        response1 = await client.post("/api/v1/auth/login", json=login_data)
        token1 = response1.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}

        # Decode first token
        payload1 = jwt.decode(
            token1,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
        version1 = payload1.get("token_version", 0)

        # Logout
        await client.post("/api/v1/auth/logout", headers=headers1)

        # Login again
        response2 = await client.post("/api/v1/auth/login", json=login_data)
        token2 = response2.json()["access_token"]

        # Decode second token
        payload2 = jwt.decode(
            token2,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
        version2 = payload2.get("token_version", 0)

        # Version should be incremented
        assert version2 > version1

        # Old token should not work
        response = await client.get("/api/v1/users/me", headers=headers1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # New token should work
        headers2 = {"Authorization": f"Bearer {token2}"}
        response = await client.get("/api/v1/users/me", headers=headers2)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_logout_all_devices_revokes_all_tokens(self, client: AsyncClient, test_user_credentials):
        """Test that logout-all-devices revokes all active tokens."""
        # Register
        await client.post("/api/v1/auth/register", json=test_user_credentials)

        login_data = {
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        }

        # Get multiple tokens (simulating different devices)
        tokens = []
        for _ in range(3):
            response = await client.post("/api/v1/auth/login", json=login_data)
            tokens.append(response.json()["access_token"])

        # Verify all tokens work
        for token in tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == status.HTTP_200_OK

        # Logout all devices using first token
        headers = {"Authorization": f"Bearer {tokens[0]}"}
        response = await client.post("/api/v1/auth/logout-all-devices", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify all tokens are now invalid
        for token in tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            assert response.json()["detail"] == "Token has been revoked"

    @pytest.mark.asyncio
    async def test_token_with_zero_version_still_validated(self, authenticated_client):
        """Test that tokens with version 0 are still validated (backward compatibility)."""
        client, token, headers = authenticated_client

        # Decode token
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )

        # Token should have a version >= 0
        assert "token_version" in payload
        assert payload["token_version"] >= 0

        # Token should work
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_200_OK

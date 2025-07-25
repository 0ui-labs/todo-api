"""Tests to verify AuthMiddleware removal doesn't break authentication."""
import pytest
from fastapi import status

from app.main import app


class TestMiddlewareCleanup:
    """Test suite for AuthMiddleware cleanup verification."""
    
    @pytest.mark.asyncio
    async def test_no_auth_middleware_in_stack(self):
        """Ensure AuthMiddleware is not in the middleware stack."""
        # Get all middleware classes
        middleware_stack = []
        
        # Try to iterate through middleware directly
        for middleware in app.user_middleware:
            if hasattr(middleware, 'cls'):
                middleware_stack.append(middleware.cls.__name__)
            else:
                middleware_stack.append(type(middleware).__name__)
                
        print(f"Found middleware: {middleware_stack}")
        
        # AuthMiddleware should not be in the stack after removal
        # This test will fail until we remove AuthMiddleware
        assert "AuthMiddleware" not in middleware_stack
        
    @pytest.mark.asyncio
    async def test_auth_still_works_on_protected_routes(
        self, client, test_user_headers: dict
    ):
        """Ensure authentication still works via dependencies on protected routes."""
        # Test with valid token
        headers = test_user_headers
        response = await client.get("/api/v1/todos/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Test without token
        response = await client.get("/api/v1/todos/")
        # Note: May get 403 due to rate limiting, but should not be 200
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid-token"}
        response = await client.get("/api/v1/todos/", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    @pytest.mark.asyncio
    async def test_public_routes_still_accessible(self, client):
        """Ensure public routes remain accessible without authentication."""
        # Health check should be public
        response = await client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        
        # Auth routes should be public
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        # Registration can have multiple valid outcomes
        assert response.status_code in [
            status.HTTP_201_CREATED,           # Success: new user created
            status.HTTP_409_CONFLICT,          # Expected: user already exists
            status.HTTP_429_TOO_MANY_REQUESTS  # Expected: rate limited
        ], f"Unexpected status code: {response.status_code}. Response: {response.json()}"
        
        # Ensure it's not requiring authentication
        assert response.status_code != status.HTTP_401_UNAUTHORIZED
        
    @pytest.mark.asyncio
    async def test_auth_logging_preserved(
        self, client, test_user_headers: dict, caplog
    ):
        """Ensure authentication events are still logged after removal."""
        # Make authenticated request
        headers = test_user_headers
        response = await client.get("/api/v1/todos/", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that request was logged (by LoggingMiddleware)
        assert any("Request started" in record.message for record in caplog.records)
        assert any("Request completed" in record.message for record in caplog.records)
        
    @pytest.mark.asyncio
    async def test_invalid_auth_scheme_handled(self, client):
        """Ensure invalid auth schemes are properly rejected."""
        # Test with Basic auth instead of Bearer
        headers = {"Authorization": "Basic dXNlcjpwYXNz"}  # user:pass in base64
        response = await client.get("/api/v1/todos/", headers=headers)
        # Note: May get 403 due to rate limiting, but should not be 200
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        
        # Test with no scheme
        headers = {"Authorization": "just-a-token"}
        response = await client.get("/api/v1/todos/", headers=headers)
        # Note: May get 403 due to rate limiting, but should not be 200
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
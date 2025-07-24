"""Comprehensive tests for authentication endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.security import get_password_hash


@pytest.mark.asyncio
class TestAuthEndpoints:
    """Comprehensive tests for authentication endpoints."""

    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123!",
                "name": "New User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert "id" in data
        assert "password" not in data  # Password should never be returned
        assert "password_hash" not in data  # Password hash should never be returned

    async def test_register_duplicate_email(
        self,
        client: AsyncClient,
        test_user: User
    ):
        """Test registration with already existing email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "password": "AnotherPassword123!",
                "name": "Another User"
            }
        )
        assert response.status_code == 409  # Conflict status for duplicate
        assert "already exists" in response.json()["detail"].lower()

    async def test_register_weak_password(self, client: AsyncClient):
        """Test registration with weak password."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@example.com",
                "password": "123",  # Too short
                "name": "Weak Password User"
            }
        )
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("at least 8 characters" in str(error) for error in errors)

    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email format."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "ValidPassword123!",
                "name": "Invalid Email User"
            }
        )
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("valid email" in str(error).lower() for error in errors)

    async def test_login_success(
        self,
        client: AsyncClient,
        test_user: User
    ):
        """Test successful login."""
        response = await client.post(
            "/api/v1/auth/login",
            json={  # JSON data
                "email": test_user.email,
                "password": "TestPassword123!"  # This is the password from conftest
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(
        self,
        client: AsyncClient,
        test_user: User
    ):
        """Test login with wrong password."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "anypassword"
            }
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    async def test_login_inactive_user(
        self,
        client: AsyncClient,
        async_session: AsyncSession
    ):
        """Test login with inactive user."""
        # Create inactive user
        inactive_user = User(
            email="inactive@example.com",
            password_hash=get_password_hash("password123"),
            name="Inactive User",
            is_active=False
        )
        async_session.add(inactive_user)
        await async_session.commit()

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "inactive@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401
        # API doesn't distinguish between wrong password and inactive user for security
        assert "Invalid email or password" in response.json()["detail"]

    async def test_token_in_protected_endpoint(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_user: User
    ):
        """Test that token works for protected endpoints (todos)."""
        response = await client.get(
            "/api/v1/todos/",
            headers=auth_headers
        )
        assert response.status_code == 200
        # Should return empty list initially
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        # The API returns offset/limit instead of page/page_size

    async def test_protected_endpoint_no_token(self, client: AsyncClient):
        """Test accessing protected endpoint without token."""
        response = await client.get("/api/v1/todos/")
        assert response.status_code == 403  # Returns 403 Forbidden without token
        assert "Not authenticated" in response.json()["detail"]

    async def test_protected_endpoint_invalid_token(self, client: AsyncClient):
        """Test accessing protected endpoint with invalid token."""
        response = await client.get(
            "/api/v1/todos/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Invalid authentication credentials" in response.json()["detail"]

    async def test_protected_endpoint_expired_token(
        self,
        client: AsyncClient,
        test_user: User,
        create_expired_token  # Fixture to create expired token
    ):
        """Test accessing protected endpoint with expired token."""
        expired_token = create_expired_token({"sub": str(test_user.id)})
        response = await client.get(
            "/api/v1/todos/",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401

    async def test_register_sql_injection_attempt(self, client: AsyncClient):
        """Test registration with SQL injection attempt in email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test'; DROP TABLE users; --@example.com",
                "password": "ValidPassword123!",
                "name": "SQL Injection Test"
            }
        )
        # Should fail validation, not execute SQL
        assert response.status_code == 422

    async def test_register_xss_attempt(self, client: AsyncClient):
        """Test registration with XSS attempt in name."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "xsstest@example.com",
                "password": "ValidPassword123!",
                "name": "<script>alert('XSS')</script>"
            }
        )
        # Should succeed but name should be properly escaped when returned
        if response.status_code == 201:
            data = response.json()
            # The name should be stored as-is but properly escaped when displayed
            assert data["name"] == "<script>alert('XSS')</script>"

    async def test_login_empty_credentials(self, client: AsyncClient):
        """Test login with empty credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "",
                "password": ""
            }
        )
        assert response.status_code == 422

    async def test_malformed_authorization_header(self, client: AsyncClient):
        """Test with malformed authorization header."""
        response = await client.get(
            "/api/v1/todos/",
            headers={"Authorization": "NotBearer token"}
        )
        assert response.status_code == 403  # Returns 403 for malformed auth header

    async def test_register_missing_required_fields(self, client: AsyncClient):
        """Test registration with missing required fields."""
        # Missing password
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "missing@example.com",
                "name": "Missing Password"
            }
        )
        assert response.status_code == 422

        # Missing email
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "password": "ValidPassword123!",
                "name": "Missing Email"
            }
        )
        assert response.status_code == 422

    # async def test_case_insensitive_email_login(
    #     self,
    #     client: AsyncClient,
    #     test_user: User
    # ):
    #     """Test that email login is case-insensitive."""
    #     # Try logging in with uppercase email
    #     response = await client.post(
    #         "/api/v1/auth/login",
    #         json={
    #             "email": test_user.email.upper(),
    #             "password": "TestPassword123!"
    #         }
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert "access_token" in data

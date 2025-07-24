"""Integration tests for authentication with rate limiting."""


import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.login_rate_limit import LoginRateLimitService
from app.utils.security import get_password_hash


@pytest.mark.asyncio
class TestAuthRateLimit:
    """Test authentication endpoints with rate limiting."""

    async def test_successful_login_clears_failed_attempts(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that successful login clears any previous failed attempts."""
        # Create test user
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("correct_password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        # First, make some failed attempts
        for _ in range(3):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "test@example.com", "password": "wrong_password"},
            )
            assert response.status_code == 401

        # Now login successfully
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "correct_password"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # Verify we can fail again without immediate lockout
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrong_password"},
        )
        assert response.status_code == 401
        assert response.json()["detail"]["remaining_attempts"] == 4

    async def test_failed_login_attempts_tracking(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that failed login attempts are properly tracked."""
        # Create test user
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("correct_password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        # Make failed attempts and check the count
        for i in range(1, 5):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "test@example.com", "password": "wrong_password"},
            )
            assert response.status_code == 401
            data = response.json()
            assert data["detail"]["failed_attempts"] == i
            assert data["detail"]["remaining_attempts"] == 5 - i

    async def test_account_lockout_after_max_attempts(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that account gets locked after maximum failed attempts."""
        # Create test user
        user = User(
            email="lockout@example.com",
            password_hash=get_password_hash("correct_password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        # Make max failed attempts
        for i in range(5):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "lockout@example.com", "password": "wrong_password"},
            )

            if i < 4:
                assert response.status_code == 401
            else:
                # 5th attempt should trigger lockout
                assert response.status_code == 429
                data = response.json()
                assert "locked_until" in data["detail"]
                assert "remaining_seconds" in data["detail"]
                assert data["detail"]["failed_attempts"] == 5
                assert "Retry-After" in response.headers

    async def test_locked_account_prevents_login(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that locked account cannot login even with correct password."""
        # Create test user
        user = User(
            email="locked@example.com",
            password_hash=get_password_hash("correct_password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        # Lock the account
        for _ in range(5):
            await client.post(
                "/api/v1/auth/login",
                json={"email": "locked@example.com", "password": "wrong_password"},
            )

        # Try to login with correct password
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "locked@example.com", "password": "correct_password"},
        )
        assert response.status_code == 429
        data = response.json()
        assert "locked_until" in data["detail"]

    async def test_admin_can_unlock_account(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_headers: dict,
    ):
        """Test that admin can unlock a locked account."""
        # Create and lock a user account
        user = User(
            email="unlock@example.com",
            password_hash=get_password_hash("password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        # Lock the account
        for _ in range(5):
            await client.post(
                "/api/v1/auth/login",
                json={"email": "unlock@example.com", "password": "wrong"},
            )

        # Admin unlocks the account
        response = await client.post(
            "/api/v1/admin/unlock-account",
            json={"email": "unlock@example.com"},
            headers=admin_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # User can now login
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "unlock@example.com", "password": "password"},
        )
        assert response.status_code == 200

    async def test_admin_can_view_locked_accounts(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_headers: dict,
    ):
        """Test that admin can view list of locked accounts."""
        # Create and lock multiple accounts
        for i in range(3):
            user = User(
                email=f"locked{i}@example.com",
                password_hash=get_password_hash("password"),
                name=f"Locked User {i}",
            )
            db_session.add(user)
        await db_session.commit()

        # Lock all accounts
        for i in range(3):
            for _ in range(5):
                await client.post(
                    "/api/v1/auth/login",
                    json={"email": f"locked{i}@example.com", "password": "wrong"},
                )

        # Get locked accounts list
        response = await client.get(
            "/api/v1/admin/locked-accounts",
            headers=admin_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

        # Verify account details
        emails = [account["email"] for account in data]
        for i in range(3):
            assert f"locked{i}@example.com" in emails

    async def test_non_admin_cannot_access_admin_endpoints(
        self,
        client: AsyncClient,
        test_user_headers: dict,
    ):
        """Test that non-admin users cannot access admin endpoints."""
        # Try to get locked accounts
        response = await client.get(
            "/api/v1/admin/locked-accounts",
            headers=test_user_headers,
        )
        assert response.status_code == 403

        # Try to unlock account
        response = await client.post(
            "/api/v1/admin/unlock-account",
            json={"email": "test@example.com"},
            headers=test_user_headers,
        )
        assert response.status_code == 403

    async def test_exponential_backoff_increases_lockout_time(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that subsequent lockouts have increasing durations."""
        # Create test user
        user = User(
            email="backoff@example.com",
            password_hash=get_password_hash("password"),
            name="Test User",
        )
        db_session.add(user)
        await db_session.commit()

        lockout_times = []

        # First lockout (5 attempts)
        for _ in range(5):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "backoff@example.com", "password": "wrong"},
            )

        data = response.json()
        lockout_times.append(data["detail"]["remaining_seconds"])

        # Clear the lockout manually for testing
        rate_limit_service = LoginRateLimitService()
        await rate_limit_service.unlock_account("backoff@example.com")
        await rate_limit_service.close()

        # Second lockout (10 attempts total)
        for _ in range(10):
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "backoff@example.com", "password": "wrong"},
            )

        data = response.json()
        lockout_times.append(data["detail"]["remaining_seconds"])

        # Second lockout should be longer than first
        assert lockout_times[1] > lockout_times[0]

    async def test_rate_limit_by_email_not_ip(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
    ):
        """Test that rate limiting is per email, not per IP."""
        # Create two users
        for email in ["user1@example.com", "user2@example.com"]:
            user = User(
                email=email,
                password_hash=get_password_hash("password"),
                name="Test User",
            )
            db_session.add(user)
        await db_session.commit()

        # Make 4 failed attempts for user1
        for _ in range(4):
            await client.post(
                "/api/v1/auth/login",
                json={"email": "user1@example.com", "password": "wrong"},
            )

        # user2 should still have all attempts available
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "user2@example.com", "password": "wrong"},
        )
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["failed_attempts"] == 1
        assert data["detail"]["remaining_attempts"] == 4

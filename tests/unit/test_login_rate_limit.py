"""Unit tests for login rate limiting service."""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
import redis.asyncio as redis
from freezegun import freeze_time

from app.services.login_rate_limit import LoginRateLimitService


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    mock = AsyncMock(spec=redis.Redis)
    # Set up default return values
    mock.get.return_value = None
    mock.exists.return_value = False
    mock.incr.return_value = 1
    mock.setex.return_value = True
    mock.expire.return_value = True
    mock.delete.return_value = True
    mock.scan.return_value = (0, [])
    return mock


@pytest.fixture
def rate_limit_service(mock_redis):
    """Create a LoginRateLimitService instance with mock Redis."""
    return LoginRateLimitService(redis_client=mock_redis)


class TestLoginRateLimitService:
    """Test cases for LoginRateLimitService."""

    @pytest.mark.asyncio
    async def test_record_failed_attempt_first_attempt(
        self, rate_limit_service, mock_redis
    ):
        """Test recording the first failed login attempt."""
        email = "test@example.com"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 1

        attempts, lockout = await rate_limit_service.record_failed_attempt(email)

        assert attempts == 1
        assert lockout is None
        mock_redis.incr.assert_called_once_with(f"failed_attempts:{email}")
        mock_redis.expire.assert_called_once()

    @pytest.mark.asyncio
    async def test_record_failed_attempt_below_threshold(
        self, rate_limit_service, mock_redis
    ):
        """Test recording failed attempts below the lockout threshold."""
        email = "test@example.com"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 3

        attempts, lockout = await rate_limit_service.record_failed_attempt(email)

        assert attempts == 3
        assert lockout is None
        mock_redis.incr.assert_called_once()

    @pytest.mark.asyncio
    @freeze_time("2025-01-24 12:00:00")
    async def test_record_failed_attempt_triggers_lockout(
        self, rate_limit_service, mock_redis
    ):
        """Test that reaching max attempts triggers account lockout."""
        email = "test@example.com"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 5  # Max attempts reached

        attempts, lockout = await rate_limit_service.record_failed_attempt(email)

        assert attempts == 5
        assert lockout is not None
        assert lockout > datetime.utcnow()

        # Verify lockout was set
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args
        assert call_args[0][0] == f"account_locked:{email}"
        assert call_args[0][1] == 60  # 1 minute lockout

    @pytest.mark.asyncio
    @freeze_time("2025-01-24 12:00:00")
    async def test_exponential_backoff(self, rate_limit_service, mock_redis):
        """Test exponential backoff calculation for lockout duration."""
        email = "test@example.com"
        mock_redis.get.return_value = None

        # Test different attempt counts and expected lockout durations
        test_cases = [
            (5, 1),    # 5 attempts = 1 minute
            (10, 2),   # 10 attempts = 2 minutes
            (15, 4),   # 15 attempts = 4 minutes
            (20, 8),   # 20 attempts = 8 minutes
            (25, 16),  # 25 attempts = 16 minutes
        ]

        for attempts, expected_minutes in test_cases:
            mock_redis.incr.return_value = attempts
            _, lockout = await rate_limit_service.record_failed_attempt(email)

            if lockout:
                lockout_duration = (lockout - datetime.utcnow()).total_seconds() / 60
                assert lockout_duration == pytest.approx(expected_minutes, rel=0.1)

    @pytest.mark.asyncio
    async def test_check_rate_limit_not_locked(self, rate_limit_service, mock_redis):
        """Test checking rate limit for unlocked account."""
        email = "test@example.com"
        mock_redis.get.side_effect = [None, "3"]  # Not locked, 3 attempts

        is_allowed, lockout, attempts = await rate_limit_service.check_rate_limit(email)

        assert is_allowed is True
        assert lockout is None
        assert attempts == 3

    @pytest.mark.asyncio
    @freeze_time("2025-01-24 12:00:00")
    async def test_check_rate_limit_locked(self, rate_limit_service, mock_redis):
        """Test checking rate limit for locked account."""
        email = "test@example.com"
        lockout_time = datetime.utcnow() + timedelta(minutes=5)
        mock_redis.get.side_effect = [lockout_time.isoformat(), "5"]

        is_allowed, lockout, attempts = await rate_limit_service.check_rate_limit(email)

        assert is_allowed is False
        assert lockout == lockout_time
        assert attempts == 5

    @pytest.mark.asyncio
    @freeze_time("2025-01-24 12:00:00")
    async def test_check_rate_limit_expired_lockout(
        self, rate_limit_service, mock_redis
    ):
        """Test that expired lockouts are cleared."""
        email = "test@example.com"
        expired_time = datetime.utcnow() - timedelta(minutes=1)
        mock_redis.get.side_effect = [expired_time.isoformat(), "0"]

        is_allowed, lockout, attempts = await rate_limit_service.check_rate_limit(email)

        assert is_allowed is True
        assert lockout is None
        assert attempts == 0
        mock_redis.delete.assert_called_once_with(f"account_locked:{email}")

    @pytest.mark.asyncio
    async def test_clear_failed_attempts(self, rate_limit_service, mock_redis):
        """Test clearing failed attempts after successful login."""
        email = "test@example.com"

        await rate_limit_service.clear_failed_attempts(email)

        mock_redis.delete.assert_called_once_with(
            f"failed_attempts:{email}",
            f"account_locked:{email}"
        )

    @pytest.mark.asyncio
    async def test_unlock_account_success(self, rate_limit_service, mock_redis):
        """Test manually unlocking a locked account."""
        email = "test@example.com"
        mock_redis.exists.return_value = True

        was_unlocked = await rate_limit_service.unlock_account(email)

        assert was_unlocked is True
        mock_redis.delete.assert_called_once_with(
            f"account_locked:{email}",
            f"failed_attempts:{email}"
        )

    @pytest.mark.asyncio
    async def test_unlock_account_not_locked(self, rate_limit_service, mock_redis):
        """Test unlocking an account that wasn't locked."""
        email = "test@example.com"
        mock_redis.exists.return_value = False

        was_unlocked = await rate_limit_service.unlock_account(email)

        assert was_unlocked is False

    @pytest.mark.asyncio
    @freeze_time("2025-01-24 12:00:00")
    async def test_get_locked_accounts(self, rate_limit_service, mock_redis):
        """Test retrieving list of locked accounts."""
        # Mock scan to return locked account keys
        mock_redis.scan.side_effect = [
            (100, [
                "account_locked:user1@example.com",
                "account_locked:user2@example.com"
            ]),
            (0, ["account_locked:user3@example.com"])
        ]

        # Mock lockout times
        future_time = datetime.utcnow() + timedelta(minutes=10)
        past_time = datetime.utcnow() - timedelta(minutes=5)

        mock_redis.get.side_effect = [
            future_time.isoformat(),  # user1 - still locked
            "5",  # user1 attempts
            past_time.isoformat(),    # user2 - expired
            future_time.isoformat(),  # user3 - still locked
            "10"  # user3 attempts
        ]

        locked_accounts = await rate_limit_service.get_locked_accounts()

        assert len(locked_accounts) == 2
        assert locked_accounts[0]["email"] == "user1@example.com"
        assert locked_accounts[0]["failed_attempts"] == 5
        assert locked_accounts[1]["email"] == "user3@example.com"
        assert locked_accounts[1]["failed_attempts"] == 10

    @pytest.mark.asyncio
    async def test_redis_error_handling_record_attempt(
        self, rate_limit_service, mock_redis
    ):
        """Test that Redis errors don't block login attempts."""
        email = "test@example.com"
        mock_redis.incr.side_effect = redis.RedisError("Connection failed")

        attempts, lockout = await rate_limit_service.record_failed_attempt(email)

        assert attempts == 0
        assert lockout is None

    @pytest.mark.asyncio
    async def test_redis_error_handling_check_limit(
        self, rate_limit_service, mock_redis
    ):
        """Test that Redis errors allow login attempts."""
        email = "test@example.com"
        mock_redis.get.side_effect = redis.RedisError("Connection failed")

        is_allowed, lockout, attempts = await rate_limit_service.check_rate_limit(email)

        assert is_allowed is True
        assert lockout is None
        assert attempts == 0

    @pytest.mark.asyncio
    async def test_max_lockout_duration(self, rate_limit_service, mock_redis):
        """Test that lockout duration doesn't exceed maximum."""
        email = "test@example.com"
        mock_redis.get.return_value = None
        mock_redis.incr.return_value = 100  # Very high attempt count

        _, lockout = await rate_limit_service.record_failed_attempt(email)

        if lockout:
            lockout_duration = (lockout - datetime.utcnow()).total_seconds() / 60
            assert lockout_duration <= rate_limit_service.max_lockout_minutes

    @pytest.mark.asyncio
    async def test_close_connection(self, rate_limit_service, mock_redis):
        """Test closing Redis connection."""
        await rate_limit_service.close()
        mock_redis.close.assert_called_once()

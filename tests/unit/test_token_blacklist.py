"""Unit tests for token blacklist service."""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
from redis.exceptions import RedisError

from app.services.token_blacklist import TokenBlacklistService


class TestTokenBlacklistService:
    """Test cases for TokenBlacklistService."""

    @pytest.fixture
    def mock_redis(self):
        """Create a mock Redis client."""
        mock = AsyncMock()
        # Set up default return values
        mock.setex = AsyncMock(return_value=True)
        mock.exists = AsyncMock(return_value=0)
        mock.get = AsyncMock(return_value=None)
        mock.incr = AsyncMock(return_value=1)
        mock.expire = AsyncMock(return_value=True)
        return mock

    @pytest.fixture
    def blacklist_service(self, mock_redis):
        """Create a TokenBlacklistService with mocked Redis."""
        return TokenBlacklistService(redis_client=mock_redis)

    @pytest.mark.asyncio
    async def test_add_token_to_blacklist_with_expiry(
        self, blacklist_service, mock_redis
    ):
        """Test adding a token to blacklist with expiration."""
        jti = str(uuid.uuid4())
        user_id = "test-user-123"
        exp = datetime.now(UTC) + timedelta(hours=1)

        await blacklist_service.add_token_to_blacklist(jti, user_id, exp)

        # Verify Redis setex was called
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args

        # Check key format
        assert call_args[0][0] == f"token_blacklist:{jti}"

        # Check TTL is approximately correct (3600 seconds + 300 buffer)
        assert 3800 <= call_args[0][1] <= 3910

        # Check data contains required fields
        import json
        data = json.loads(call_args[0][2])
        assert data["user_id"] == user_id
        assert data["jti"] == jti
        assert "revoked_at" in data

    @pytest.mark.asyncio
    async def test_add_token_to_blacklist_without_expiry(
        self, blacklist_service, mock_redis
    ):
        """Test adding a token to blacklist without expiration."""
        jti = str(uuid.uuid4())
        user_id = "test-user-123"

        await blacklist_service.add_token_to_blacklist(jti, user_id)

        # Verify Redis setex was called with default TTL
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args

        # Check default TTL (24 hours)
        assert call_args[0][1] == 86400

    @pytest.mark.asyncio
    async def test_add_token_to_blacklist_expired_token(
        self, blacklist_service, mock_redis
    ):
        """Test adding an already expired token to blacklist."""
        jti = str(uuid.uuid4())
        user_id = "test-user-123"
        exp = datetime.now(UTC) - timedelta(hours=1)  # Already expired

        await blacklist_service.add_token_to_blacklist(jti, user_id, exp)

        # Should still add with default TTL since token is expired
        mock_redis.setex.assert_called_once()
        call_args = mock_redis.setex.call_args
        assert call_args[0][1] == 86400  # Default TTL

    @pytest.mark.asyncio
    async def test_is_token_blacklisted_true(self, blacklist_service, mock_redis):
        """Test checking if a token is blacklisted (found case)."""
        jti = str(uuid.uuid4())
        mock_redis.exists.return_value = 1

        result = await blacklist_service.is_token_blacklisted(jti)

        assert result is True
        mock_redis.exists.assert_called_once_with(f"token_blacklist:{jti}")

    @pytest.mark.asyncio
    async def test_is_token_blacklisted_false(self, blacklist_service, mock_redis):
        """Test checking if a token is blacklisted (not found case)."""
        jti = str(uuid.uuid4())
        mock_redis.exists.return_value = 0

        result = await blacklist_service.is_token_blacklisted(jti)

        assert result is False
        mock_redis.exists.assert_called_once_with(f"token_blacklist:{jti}")

    @pytest.mark.asyncio
    async def test_is_token_blacklisted_redis_error(
        self, blacklist_service, mock_redis
    ):
        """Test token blacklist check fails closed on Redis error."""
        jti = str(uuid.uuid4())
        mock_redis.exists.side_effect = RedisError("Connection failed")

        # Should fail closed (return True) on error
        result = await blacklist_service.is_token_blacklisted(jti)

        assert result is True

    @pytest.mark.asyncio
    async def test_revoke_all_user_tokens(self, blacklist_service, mock_redis):
        """Test revoking all tokens for a user."""
        user_id = "test-user-123"

        await blacklist_service.revoke_all_user_tokens(user_id)

        # Verify token version was incremented
        mock_redis.incr.assert_called_once_with(f"user_token_version:{user_id}")

        # Verify TTL was set
        mock_redis.expire.assert_called_once_with(
            f"user_token_version:{user_id}",
            30 * 86400  # 30 days
        )

    @pytest.mark.asyncio
    async def test_get_user_token_version_exists(self, blacklist_service, mock_redis):
        """Test getting user token version when it exists."""
        user_id = "test-user-123"
        mock_redis.get.return_value = "5"

        version = await blacklist_service.get_user_token_version(user_id)

        assert version == 5
        mock_redis.get.assert_called_once_with(f"user_token_version:{user_id}")

    @pytest.mark.asyncio
    async def test_get_user_token_version_not_exists(
        self, blacklist_service, mock_redis
    ):
        """Test getting user token version when it doesn't exist."""
        user_id = "test-user-123"
        mock_redis.get.return_value = None

        version = await blacklist_service.get_user_token_version(user_id)

        assert version == 0

    @pytest.mark.asyncio
    async def test_get_user_token_version_redis_error(
        self, blacklist_service, mock_redis
    ):
        """Test getting user token version returns 0 on Redis error."""
        user_id = "test-user-123"
        mock_redis.get.side_effect = RedisError("Connection failed")

        version = await blacklist_service.get_user_token_version(user_id)

        assert version == 0

    @pytest.mark.asyncio
    async def test_cleanup_expired_entries(self, blacklist_service):
        """Test cleanup method (no-op for Redis TTL)."""
        result = await blacklist_service.cleanup_expired_entries()
        assert result == 0

    @pytest.mark.asyncio
    async def test_close_connection(self, blacklist_service, mock_redis):
        """Test closing Redis connection."""
        await blacklist_service.close()
        mock_redis.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_redis_creates_client_once(self):
        """Test that Redis client is created only once."""
        with patch('app.services.token_blacklist.redis.from_url') as mock_from_url:
            mock_client = AsyncMock()
            # Make from_url return a coroutine
            async def async_from_url(*args, **kwargs):
                return mock_client
            mock_from_url.side_effect = async_from_url

            service = TokenBlacklistService()

            # Call _get_redis multiple times
            client1 = await service._get_redis()
            client2 = await service._get_redis()

            # Should only create client once
            mock_from_url.assert_called_once()
            assert client1 is client2

    @pytest.mark.asyncio
    async def test_add_token_redis_error_propagates(
        self, blacklist_service, mock_redis
    ):
        """Test that Redis errors in add_token_to_blacklist are propagated."""
        jti = str(uuid.uuid4())
        user_id = "test-user-123"
        mock_redis.setex.side_effect = RedisError("Connection failed")

        with pytest.raises(RedisError):
            await blacklist_service.add_token_to_blacklist(jti, user_id)

    @pytest.mark.asyncio
    async def test_revoke_all_tokens_redis_error_propagates(
        self, blacklist_service, mock_redis
    ):
        """Test that Redis errors in revoke_all_user_tokens are propagated."""
        user_id = "test-user-123"
        mock_redis.incr.side_effect = RedisError("Connection failed")

        with pytest.raises(RedisError):
            await blacklist_service.revoke_all_user_tokens(user_id)

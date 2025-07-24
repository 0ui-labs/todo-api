"""Token blacklist service for JWT revocation."""

import json
from datetime import UTC, datetime

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.config import settings
from app.redis import get_redis_client


class TokenBlacklistService:
    """Service for managing JWT token blacklist/revocation."""

    def __init__(self, redis_client: redis.Redis | None = None):
        """Initialize the token blacklist service.

        Args:
            redis_client: Optional Redis client instance. If not provided,
                         creates a new one from settings.
        """
        self._redis = redis_client
        self._prefix = "token_blacklist:"
        self._user_version_prefix = "user_token_version:"

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._redis is None:
            self._redis = await get_redis_client(settings.redis_db)
        return self._redis

    async def add_token_to_blacklist(
        self,
        jti: str,
        user_id: str,
        exp: datetime | None = None
    ) -> None:
        """Add a token to the blacklist.

        Args:
            jti: JWT ID (unique identifier for the token)
            user_id: User ID associated with the token
            exp: Token expiration time. If provided, sets TTL on the blacklist entry.
        """
        try:
            client = await self._get_redis()
            key = f"{self._prefix}{jti}"

            # Store token metadata
            data = {
                "user_id": user_id,
                "revoked_at": datetime.now(UTC).isoformat(),
                "jti": jti
            }

            # Calculate TTL if expiration is provided
            ttl = None
            if exp:
                ttl_seconds = int((exp - datetime.now(UTC)).total_seconds())
                # Only set TTL if token hasn't already expired
                if ttl_seconds > 0:
                    ttl = ttl_seconds + 300  # Add 5 minutes buffer

            # Store in Redis with optional TTL
            if ttl:
                await client.setex(key, ttl, json.dumps(data))
            else:
                # Default TTL of 24 hours for tokens without expiration
                await client.setex(key, 86400, json.dumps(data))

        except RedisError as e:
            # Log error but don't fail - security should not depend solely on blacklist
            print(f"Redis error adding token to blacklist: {e}")
            raise

    async def is_token_blacklisted(self, jti: str) -> bool:
        """Check if a token is blacklisted.

        Args:
            jti: JWT ID to check

        Returns:
            True if token is blacklisted, False otherwise
        """
        try:
            client = await self._get_redis()
            key = f"{self._prefix}{jti}"
            result = await client.exists(key)
            return bool(result)
        except RedisError as e:
            # On Redis error, fail closed (treat as blacklisted for security)
            print(f"Redis error checking blacklist: {e}")
            return True

    async def revoke_all_user_tokens(self, user_id: str) -> None:
        """Revoke all tokens for a user by incrementing their token version.

        This is more efficient than blacklisting individual tokens when
        a user wants to logout from all devices.

        Args:
            user_id: User ID whose tokens should be revoked
        """
        try:
            client = await self._get_redis()
            key = f"{self._user_version_prefix}{user_id}"

            # Increment the user's token version
            await client.incr(key)

            # Set TTL to match max token lifetime
            ttl_days = 30  # Adjust based on your token lifetime
            await client.expire(key, ttl_days * 86400)

        except RedisError as e:
            print(f"Redis error revoking user tokens: {e}")
            raise

    async def get_user_token_version(self, user_id: str) -> int:
        """Get the current token version for a user.

        Args:
            user_id: User ID to check

        Returns:
            Current token version (0 if not set)
        """
        try:
            client = await self._get_redis()
            key = f"{self._user_version_prefix}{user_id}"
            version = await client.get(key)
            return int(version) if version else 0
        except RedisError as e:
            print(f"Redis error getting user token version: {e}")
            # On error, return 0 to allow tokens to work
            return 0

    async def cleanup_expired_entries(self) -> int:
        """Clean up expired blacklist entries.

        This is handled automatically by Redis TTL, but this method
        can be used for manual cleanup if needed.

        Returns:
            Number of entries cleaned up
        """
        # Redis handles TTL automatically, so this is a no-op
        # Kept for API compatibility
        return 0

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._redis:
            await self._redis.close()


# Global instance
_blacklist_service: TokenBlacklistService | None = None


async def get_token_blacklist_service() -> TokenBlacklistService:
    """Get the global token blacklist service instance."""
    global _blacklist_service
    if _blacklist_service is None:
        _blacklist_service = TokenBlacklistService()
    return _blacklist_service

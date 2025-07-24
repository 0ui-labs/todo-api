"""Redis-based caching service for API responses."""
import hashlib
import json
from collections.abc import Callable
from typing import Any

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.config import settings
from app.redis import get_redis_client
from app.monitoring.metrics import (
    cache_deletes_total,
    cache_hits_total,
    cache_misses_total,
    cache_sets_total,
)


class CacheService:
    """Service for caching API responses and frequently accessed data."""

    def __init__(self, redis_client: redis.Redis | None = None):
        """Initialize the cache service.

        Args:
            redis_client: Optional Redis client instance. If not provided,
                         creates a new one from settings.
        """
        self._redis = redis_client
        self._prefix = "cache:"
        # Use a dedicated DB for cache (different from rate limiting)
        self._cache_db = 2  # Using DB 2 for cache

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._redis is None:
            self._redis = await get_redis_client(self._cache_db)
        return self._redis

    def _make_key(self, namespace: str, key: str) -> str:
        """Create a cache key with namespace."""
        return f"{self._prefix}{namespace}:{key}"

    def _hash_dict(self, data: dict) -> str:
        """Create a hash from dictionary for cache key."""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True)
        return hashlib.md5(sorted_data.encode()).hexdigest()

    async def get(self, namespace: str, key: str) -> Any | None:
        """Get value from cache.

        Args:
            namespace: Cache namespace (e.g., 'todos', 'categories')
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            client = await self._get_redis()
            cache_key = self._make_key(namespace, key)
            value = await client.get(cache_key)

            if value:
                cache_hits_total.labels(namespace=namespace).inc()
                return json.loads(value)
            cache_misses_total.labels(namespace=namespace).inc()
            return None

        except (RedisError, json.JSONDecodeError) as e:
            # Log error but don't fail the request
            print(f"Cache get error: {e}")
            return None

    async def set(
        self,
        namespace: str,
        key: str,
        value: Any,
        ttl: int = 300
    ) -> bool:
        """Set value in cache with TTL.

        Args:
            namespace: Cache namespace
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (default: 5 minutes)

        Returns:
            True if successful, False otherwise
        """
        try:
            client = await self._get_redis()
            cache_key = self._make_key(namespace, key)
            serialized = json.dumps(value)

            await client.setex(cache_key, ttl, serialized)
            cache_sets_total.labels(namespace=namespace).inc()
            return True

        except (RedisError, TypeError) as e:
            # Log error but don't fail the request
            print(f"Cache set error: {e}")
            return False

    async def delete(self, namespace: str, key: str) -> bool:
        """Delete value from cache.

        Args:
            namespace: Cache namespace
            key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        try:
            client = await self._get_redis()
            cache_key = self._make_key(namespace, key)
            result = await client.delete(cache_key)
            if result:
                cache_deletes_total.labels(namespace=namespace).inc()
            return bool(result)

        except RedisError as e:
            print(f"Cache delete error: {e}")
            return False

    async def delete_pattern(self, namespace: str, pattern: str) -> int:
        """Delete all keys matching a pattern.

        Args:
            namespace: Cache namespace
            pattern: Pattern to match (e.g., 'user:*')

        Returns:
            Number of keys deleted
        """
        try:
            client = await self._get_redis()
            pattern_key = self._make_key(namespace, pattern)

            # Find all matching keys
            keys = []
            async for key in client.scan_iter(match=pattern_key):
                keys.append(key)

            # Delete all found keys
            if keys:
                deleted_count = await client.delete(*keys)
                cache_deletes_total.labels(namespace=namespace).inc(deleted_count)
                return deleted_count
            return 0

        except RedisError as e:
            print(f"Cache delete pattern error: {e}")
            return 0

    async def invalidate_user_cache(self, user_id: str) -> None:
        """Invalidate all cache entries for a specific user.

        Args:
            user_id: User ID to invalidate cache for
        """
        # Invalidate todos
        await self.delete_pattern("todos", f"user:{user_id}:*")
        # Invalidate categories
        await self.delete_pattern("categories", f"user:{user_id}:*")
        # Invalidate user-specific data
        await self.delete_pattern("user", f"{user_id}:*")

    async def get_or_set(
        self,
        namespace: str,
        key: str,
        factory: Callable,
        ttl: int = 300
    ) -> Any:
        """Get from cache or compute and cache the value.

        Args:
            namespace: Cache namespace
            key: Cache key
            factory: Async function to compute value if not cached
            ttl: Time to live in seconds

        Returns:
            Cached or computed value
        """
        # Try to get from cache first
        value = await self.get(namespace, key)
        if value is not None:
            return value

        # Compute value
        value = await factory()

        # Cache it
        await self.set(namespace, key, value, ttl)

        return value

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._redis:
            await self._redis.close()


# Global cache service instance
_cache_service: CacheService | None = None


async def get_cache_service() -> CacheService:
    """Get or create the global cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service

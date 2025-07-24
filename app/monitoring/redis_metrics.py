"""Redis metrics wrapper for tracking cache performance."""
import time
from typing import Any

import redis.asyncio as redis

from app.monitoring.metrics import (
    cache_deletes_total,
    cache_hits_total,
    cache_misses_total,
    cache_sets_total,
)


class MetricsRedisClient:
    """Redis client wrapper that tracks cache metrics."""
    
    def __init__(self, redis_client: redis.Redis, namespace: str = "default"):
        """Initialize the metrics wrapper.
        
        Args:
            redis_client: Underlying Redis client
            namespace: Namespace for metrics labeling
        """
        self._client = redis_client
        self._namespace = namespace
    
    async def get(self, key: str) -> Any:
        """Get a value from cache with metrics tracking.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        result = await self._client.get(key)
        
        if result is not None:
            cache_hits_total.labels(namespace=self._namespace).inc()
        else:
            cache_misses_total.labels(namespace=self._namespace).inc()
            
        return result
    
    async def mget(self, keys: list[str]) -> list[Any]:
        """Get multiple values with metrics tracking.
        
        Args:
            keys: List of cache keys
            
        Returns:
            List of cached values
        """
        results = await self._client.mget(keys)
        
        for result in results:
            if result is not None:
                cache_hits_total.labels(namespace=self._namespace).inc()
            else:
                cache_misses_total.labels(namespace=self._namespace).inc()
                
        return results
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ex: int | None = None,
        px: int | None = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False
    ) -> bool:
        """Set a value in cache with metrics tracking.
        
        Args:
            key: Cache key
            value: Value to cache
            ex: Expire time in seconds
            px: Expire time in milliseconds
            nx: Only set if key doesn't exist
            xx: Only set if key exists
            keepttl: Keep existing TTL
            
        Returns:
            True if set was successful
        """
        result = await self._client.set(key, value, ex=ex, px=px, nx=nx, xx=xx, keepttl=keepttl)
        
        if result:
            cache_sets_total.labels(namespace=self._namespace).inc()
            
        return result
    
    async def setex(self, key: str, seconds: int, value: Any) -> bool:
        """Set a value with expiration.
        
        Args:
            key: Cache key
            seconds: TTL in seconds
            value: Value to cache
            
        Returns:
            True if successful
        """
        result = await self._client.setex(key, seconds, value)
        
        if result:
            cache_sets_total.labels(namespace=self._namespace).inc()
            
        return result
    
    async def delete(self, *keys: str) -> int:
        """Delete keys from cache with metrics tracking.
        
        Args:
            keys: Keys to delete
            
        Returns:
            Number of keys deleted
        """
        result = await self._client.delete(*keys)
        
        if result > 0:
            cache_deletes_total.labels(namespace=self._namespace).inc(result)
            
        return result
    
    async def exists(self, *keys: str) -> int:
        """Check if keys exist.
        
        Args:
            keys: Keys to check
            
        Returns:
            Number of existing keys
        """
        return await self._client.exists(*keys)
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set TTL on a key.
        
        Args:
            key: Cache key
            seconds: TTL in seconds
            
        Returns:
            True if TTL was set
        """
        return await self._client.expire(key, seconds)
    
    async def ttl(self, key: str) -> int:
        """Get TTL of a key.
        
        Args:
            key: Cache key
            
        Returns:
            TTL in seconds, -2 if key doesn't exist, -1 if no TTL
        """
        return await self._client.ttl(key)
    
    # Delegate other methods to the underlying client
    def __getattr__(self, name: str) -> Any:
        """Delegate unknown methods to the underlying Redis client."""
        return getattr(self._client, name)


async def get_metrics_redis_client(db: int = 0, namespace: str = "default") -> MetricsRedisClient:
    """Get a Redis client with metrics tracking.
    
    Args:
        db: Redis database number
        namespace: Namespace for metrics
        
    Returns:
        MetricsRedisClient instance
    """
    from app.redis import get_redis_client
    
    client = await get_redis_client(db)
    return MetricsRedisClient(client, namespace)
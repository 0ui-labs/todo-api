"""Redis connection pool configuration and management."""

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from app.config import settings

# Global connection pools for different Redis databases
_connection_pools: dict[int, ConnectionPool] = {}


def get_redis_pool(db: int = 0) -> ConnectionPool:
    """Get or create Redis connection pool for a specific database.

    Args:
        db: Redis database number (0-15)

    Returns:
        ConnectionPool instance configured for production use
    """
    if db not in _connection_pools:
        # Parse base URL without DB number
        base_url = settings.redis_url
        if base_url.endswith(("/0", "/1", "/2", "/3", "/4", "/5", "/6", "/7",
                             "/8", "/9", "/10", "/11", "/12", "/13", "/14", "/15")):
            # Remove existing DB number
            base_url = base_url.rsplit("/", 1)[0]

        # Create pool with production-ready settings
        _connection_pools[db] = redis.ConnectionPool.from_url(
            f"{base_url}/{db}",
            decode_responses=True,
            # Connection pool settings
            max_connections=50,  # Maximum number of connections
            health_check_interval=30,  # Health check every 30 seconds
            socket_keepalive=True,  # Enable TCP keepalive
            socket_keepalive_options={
                1: 1,  # TCP_KEEPIDLE: 1 second
                2: 3,  # TCP_KEEPINTVL: 3 seconds
                3: 5,  # TCP_KEEPCNT: 5 probes
            },
            retry_on_timeout=True,  # Retry on timeout
            retry_on_error=[ConnectionError, TimeoutError],  # Retry on these errors
        )

    return _connection_pools[db]


async def get_redis_client(db: int = 0) -> redis.Redis:
    """Get Redis client with connection from pool.

    Args:
        db: Redis database number (0-15)

    Returns:
        Redis client instance using connection pool
    """
    pool = get_redis_pool(db)
    return redis.Redis(connection_pool=pool)


async def close_redis_pools():
    """Close all Redis connection pools.

    Should be called on application shutdown.
    """
    for pool in _connection_pools.values():
        await pool.aclose()
    _connection_pools.clear()

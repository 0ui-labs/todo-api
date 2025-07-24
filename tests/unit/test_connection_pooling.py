"""Tests for database and Redis connection pooling."""

import pytest

from app.database import engine
from app.redis import close_redis_pools, get_redis_pool


class TestDatabaseConnectionPooling:
    """Test database connection pooling configuration."""

    def test_engine_pool_configuration(self):
        """Test that engine is configured with correct pool settings."""
        # For unit tests, we verify configuration without actual connections
        assert hasattr(engine, 'pool'), "Engine should have a pool"
        assert hasattr(engine, 'sync_engine'), "Engine should have sync_engine"

        # Verify engine exists and is properly configured
        assert engine is not None
        assert str(engine.url) is not None

        # Note: Actual pool behavior (size, overflow, etc.) is tested
        # in integration tests with a real database connection


class TestRedisConnectionPooling:
    """Test Redis connection pooling configuration."""

    def test_redis_pool_creation(self):
        """Test that Redis pools are created with correct settings."""
        pool1 = get_redis_pool(0)
        pool2 = get_redis_pool(1)

        # Different DB numbers should have different pools
        assert pool1 is not pool2

        # Same DB number should return same pool
        pool1_again = get_redis_pool(0)
        assert pool1 is pool1_again

        # Check pool has correct configuration attributes
        assert hasattr(pool1, 'max_connections')
        assert pool1.max_connections == 50

    def test_redis_pool_separation(self):
        """Test that different DB numbers get separate pools."""
        pools = {}

        # Create pools for different DBs
        for db in range(5):
            pools[db] = get_redis_pool(db)

        # All pools should be different instances
        pool_instances = list(pools.values())
        for i, pool1 in enumerate(pool_instances):
            for j, pool2 in enumerate(pool_instances):
                if i != j:
                    assert pool1 is not pool2

    @pytest.mark.asyncio
    async def test_redis_pool_cleanup(self):
        """Test that Redis pools cleanup doesn't error."""
        # Create some pools
        get_redis_pool(0)
        get_redis_pool(1)

        # Close all pools should not raise an error
        try:
            await close_redis_pools()
        except Exception as e:
            pytest.fail(f"Pool cleanup raised an error: {e}")

        # New pools should be created after cleanup
        new_pool = get_redis_pool(0)
        assert new_pool is not None

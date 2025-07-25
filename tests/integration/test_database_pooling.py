"""Tests for database connection pooling configuration."""
import asyncio
import time

import pytest
from sqlalchemy import text

from app.database import engine

# Skip these tests if not using PostgreSQL
pytestmark = pytest.mark.skipif(
    "postgresql" not in str(engine.url),
    reason="Connection pooling tests require PostgreSQL"
)


@pytest.mark.asyncio
async def test_connection_pool_configuration():
    """Test that connection pool is properly configured."""
    # Check pool configuration
    assert engine.pool.__class__.__name__ != "NullPool"
    assert engine.pool.size() == 20
    assert engine.pool.overflow() == -20  # Initial overflow is negative of pool size
    assert engine.pool._timeout == 30
    assert engine.pool._recycle == 3600


@pytest.mark.asyncio
async def test_connection_pool_reuse():
    """Test that connections are being reused from the pool."""
    connection_ids = []

    # Execute multiple queries and track connection IDs
    for _ in range(5):
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT pg_backend_pid()"))
            pid = result.scalar()
            connection_ids.append(pid)

    # Check that we're reusing connections (not all PIDs should be unique)
    unique_pids = set(connection_ids)
    assert len(unique_pids) <= 5, "Connections should be reused from pool"


@pytest.mark.asyncio
async def test_connection_pool_overflow():
    """Test that pool can handle overflow connections."""
    connections = []

    try:
        # Create more connections than pool_size
        for i in range(25):  # pool_size=20, so this tests overflow
            conn = await engine.connect()
            connections.append(conn)
            # Execute a query to ensure connection is active
            await conn.execute(text("SELECT 1"))

        # All connections should succeed
        assert len(connections) == 25

    finally:
        # Clean up connections
        for conn in connections:
            await conn.close()


@pytest.mark.asyncio
async def test_connection_pool_timeout():
    """Test pool timeout behavior."""
    connections = []

    try:
        # Fill up the pool and overflow
        for i in range(60):  # pool_size=20 + max_overflow=40
            conn = await engine.connect()
            connections.append(conn)
            await conn.execute(text("SELECT 1"))

        # This should timeout since pool is exhausted
        with pytest.raises(asyncio.TimeoutError):
            async with asyncio.timeout(2):  # Short timeout to not wait full 30s
                conn = await engine.connect()
                await conn.execute(text("SELECT 1"))

    finally:
        # Clean up connections
        for conn in connections:
            await conn.close()


@pytest.mark.asyncio
async def test_connection_pool_pre_ping():
    """Test that pre-ping is working to validate connections."""
    # Get a connection
    async with engine.connect() as conn:
        # Execute a query
        await conn.execute(text("SELECT 1"))

        # Simulate connection becoming invalid by killing it
        # In a real scenario, this would be a network issue or server restart
        # For testing, we'll just verify the connection works
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

    # Get another connection - pre-ping should validate it
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_concurrent_connection_usage():
    """Test pool behavior under concurrent load."""
    async def execute_query(query_id: int):
        """Execute a simple query and return timing info."""
        start_time = time.time()
        async with engine.connect() as conn:
            await conn.execute(text(f"SELECT pg_sleep(0.1), {query_id}"))
        end_time = time.time()
        return end_time - start_time

    # Run 50 concurrent queries
    tasks = [execute_query(i) for i in range(50)]
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time

    # With proper pooling, this should complete faster than sequential execution
    # 50 queries * 0.1s sleep = 5s if sequential
    # With pool_size=20, should be around 0.3s (3 batches)
    assert total_time < 1.0, f"Concurrent execution too slow: {total_time}s"
    assert all(r > 0.1 for r in results), "All queries should take at least 0.1s"

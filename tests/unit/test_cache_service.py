"""Unit tests for cache service."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import redis.asyncio as redis
from redis.exceptions import RedisError

from app.services.cache import CacheService


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    mock = AsyncMock(spec=redis.Redis)
    # Make sure async methods return coroutines
    mock.get = AsyncMock()
    mock.setex = AsyncMock()
    mock.delete = AsyncMock()
    mock.scan_iter = MagicMock()
    return mock


@pytest.fixture
def cache_service(mock_redis):
    """Create a cache service with mocked Redis."""
    return CacheService(redis_client=mock_redis)


@pytest.mark.asyncio
async def test_get_cached_value(cache_service, mock_redis):
    """Test retrieving a cached value."""
    # Setup
    test_data = {"id": "123", "name": "Test"}
    mock_redis.get.return_value = json.dumps(test_data)

    # Execute
    result = await cache_service.get("todos", "test_key")

    # Verify
    assert result == test_data
    mock_redis.get.assert_called_once_with("cache:todos:test_key")


@pytest.mark.asyncio
async def test_get_cache_miss(cache_service, mock_redis):
    """Test cache miss returns None."""
    # Setup
    mock_redis.get.return_value = None

    # Execute
    result = await cache_service.get("todos", "missing_key")

    # Verify
    assert result is None
    mock_redis.get.assert_called_once_with("cache:todos:missing_key")


@pytest.mark.asyncio
async def test_get_with_redis_error(cache_service, mock_redis):
    """Test get handles Redis errors gracefully."""
    # Setup
    mock_redis.get.side_effect = RedisError("Connection failed")

    # Execute
    result = await cache_service.get("todos", "test_key")

    # Verify
    assert result is None  # Should return None on error


@pytest.mark.asyncio
async def test_set_cached_value(cache_service, mock_redis):
    """Test setting a value in cache."""
    # Setup
    test_data = {"id": "123", "name": "Test"}

    # Execute
    result = await cache_service.set("todos", "test_key", test_data, ttl=600)

    # Verify
    assert result is True
    mock_redis.setex.assert_called_once_with(
        "cache:todos:test_key",
        600,
        json.dumps(test_data)
    )


@pytest.mark.asyncio
async def test_set_with_redis_error(cache_service, mock_redis):
    """Test set handles Redis errors gracefully."""
    # Setup
    mock_redis.setex.side_effect = RedisError("Connection failed")

    # Execute
    result = await cache_service.set("todos", "test_key", {"data": "test"})

    # Verify
    assert result is False  # Should return False on error


@pytest.mark.asyncio
async def test_delete_cached_value(cache_service, mock_redis):
    """Test deleting a cached value."""
    # Setup
    mock_redis.delete.return_value = 1

    # Execute
    result = await cache_service.delete("todos", "test_key")

    # Verify
    assert result is True
    mock_redis.delete.assert_called_once_with("cache:todos:test_key")


@pytest.mark.asyncio
async def test_delete_pattern(cache_service, mock_redis):
    """Test deleting values by pattern."""
    # Setup
    async def async_generator():
        yield "cache:todos:user:123:get_todos"
        yield "cache:todos:user:123:get_todo"

    mock_redis.scan_iter.return_value = async_generator()
    mock_redis.delete.return_value = 2

    # Execute
    result = await cache_service.delete_pattern("todos", "user:123:*")

    # Verify
    assert result == 2
    mock_redis.scan_iter.assert_called_once_with(match="cache:todos:user:123:*")
    mock_redis.delete.assert_called_once_with(
        "cache:todos:user:123:get_todos",
        "cache:todos:user:123:get_todo"
    )


@pytest.mark.asyncio
async def test_invalidate_user_cache(cache_service):
    """Test invalidating all cache for a user."""
    # Setup
    with patch.object(cache_service, 'delete_pattern') as mock_delete:
        # Execute
        await cache_service.invalidate_user_cache("user123")

        # Verify
        assert mock_delete.call_count == 3
        mock_delete.assert_any_call("todos", "user:user123:*")
        mock_delete.assert_any_call("categories", "user:user123:*")
        mock_delete.assert_any_call("user", "user123:*")


@pytest.mark.asyncio
async def test_get_or_set_cache_hit(cache_service):
    """Test get_or_set with cache hit."""
    # Setup
    cached_data = {"cached": True}
    factory = AsyncMock(return_value={"fresh": True})

    with patch.object(cache_service, 'get', return_value=cached_data):
        # Execute
        result = await cache_service.get_or_set("todos", "key", factory, ttl=300)

        # Verify
        assert result == cached_data
        factory.assert_not_called()  # Factory should not be called on cache hit


@pytest.mark.asyncio
async def test_get_or_set_cache_miss(cache_service):
    """Test get_or_set with cache miss."""
    # Setup
    fresh_data = {"fresh": True}
    factory = AsyncMock(return_value=fresh_data)

    with patch.object(cache_service, 'get', return_value=None):
        with patch.object(cache_service, 'set') as mock_set:
            # Execute
            result = await cache_service.get_or_set("todos", "key", factory, ttl=300)

            # Verify
            assert result == fresh_data
            factory.assert_called_once()
            mock_set.assert_called_once_with("todos", "key", fresh_data, 300)


@pytest.mark.asyncio
async def test_make_key():
    """Test cache key generation."""
    service = CacheService()

    key = service._make_key("todos", "user:123:get_todos")
    assert key == "cache:todos:user:123:get_todos"


@pytest.mark.asyncio
async def test_hash_dict():
    """Test dictionary hashing for cache keys."""
    service = CacheService()

    # Same content, different order should produce same hash
    dict1 = {"b": 2, "a": 1, "c": 3}
    dict2 = {"a": 1, "c": 3, "b": 2}

    hash1 = service._hash_dict(dict1)
    hash2 = service._hash_dict(dict2)

    assert hash1 == hash2
    assert len(hash1) == 32  # MD5 hash length

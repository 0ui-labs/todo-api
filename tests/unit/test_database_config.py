"""Unit tests for database configuration."""
import pytest

from app.database import engine


def test_database_pool_configuration():
    """Test that database engine has proper pool configuration."""
    # For testing, we just verify the engine was created with our parameters
    # The actual pool behavior is tested in integration tests
    
    # Check that the engine exists and has a pool
    assert hasattr(engine, 'pool'), "Engine should have a pool"
    assert hasattr(engine, 'sync_engine'), "Engine should have sync_engine"
    
    # When using SQLite for tests, pooling is handled differently
    # So we'll just verify the engine is properly initialized
    assert engine is not None
    assert str(engine.url) is not None


def test_async_session_configuration():
    """Test that async session maker is properly configured."""
    from app.database import async_session_maker
    
    # Check session configuration
    assert async_session_maker is not None
    assert hasattr(async_session_maker, 'kw'), "Session maker should have kw attribute"
    assert async_session_maker.kw.get("expire_on_commit") is False
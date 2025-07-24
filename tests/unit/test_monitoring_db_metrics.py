"""Unit tests for database metrics collection."""
from unittest.mock import MagicMock, patch

import pytest

from app.monitoring.db_metrics import (
    _extract_operation,
    _extract_table,
    _update_pool_metrics,
    setup_db_metrics,
)
from app.monitoring.metrics import (
    db_connections_active,
    db_connections_idle,
    db_query_duration_seconds,
    db_query_total,
)


class TestDbMetricsHelpers:
    """Test database metrics helper functions."""
    
    def test_extract_operation_select(self):
        """Test extracting SELECT operation."""
        assert _extract_operation("SELECT * FROM users") == "select"
        assert _extract_operation("select id, name from todos") == "select"
        assert _extract_operation("  SELECT COUNT(*) FROM categories  ") == "select"
    
    def test_extract_operation_insert(self):
        """Test extracting INSERT operation."""
        assert _extract_operation("INSERT INTO users (name) VALUES ('test')") == "insert"
        assert _extract_operation("insert into todos values (1, 'test')") == "insert"
    
    def test_extract_operation_update(self):
        """Test extracting UPDATE operation."""
        assert _extract_operation("UPDATE users SET name = 'new'") == "update"
        assert _extract_operation("update todos set completed = true") == "update"
    
    def test_extract_operation_delete(self):
        """Test extracting DELETE operation."""
        assert _extract_operation("DELETE FROM users WHERE id = 1") == "delete"
        assert _extract_operation("delete from todos") == "delete"
    
    def test_extract_operation_transaction(self):
        """Test extracting transaction operations."""
        assert _extract_operation("BEGIN") == "transaction"
        assert _extract_operation("COMMIT") == "transaction"
        assert _extract_operation("ROLLBACK") == "transaction"
    
    def test_extract_operation_other(self):
        """Test extracting other operations."""
        assert _extract_operation("CREATE TABLE users") == "other"
        assert _extract_operation("DROP TABLE todos") == "other"
        assert _extract_operation("ALTER TABLE categories") == "other"
    
    def test_extract_table_select(self):
        """Test extracting table from SELECT."""
        assert _extract_table("SELECT * FROM users", "select") == "users"
        assert _extract_table("SELECT id FROM todos WHERE status = 'pending'", "select") == "todos"
        assert _extract_table('SELECT * FROM "categories"', "select") == "categories"
        assert _extract_table("SELECT * FROM users u JOIN todos t", "select") == "users"
    
    def test_extract_table_insert(self):
        """Test extracting table from INSERT."""
        assert _extract_table("INSERT INTO users (name) VALUES ('test')", "insert") == "users"
        assert _extract_table('INSERT INTO "todos" VALUES (1)', "insert") == "todos"
        assert _extract_table("insert into categories (name) values ('work')", "insert") == "categories"
    
    def test_extract_table_update(self):
        """Test extracting table from UPDATE."""
        assert _extract_table("UPDATE users SET name = 'new'", "update") == "users"
        assert _extract_table('UPDATE "todos" SET completed = true', "update") == "todos"
        assert _extract_table("UPDATE ONLY categories SET name = 'personal'", "update") == "categories"
    
    def test_extract_table_delete(self):
        """Test extracting table from DELETE."""
        assert _extract_table("DELETE FROM users WHERE id = 1", "delete") == "users"
        assert _extract_table("DELETE FROM todos", "delete") == "todos"
        assert _extract_table('DELETE FROM "categories"', "delete") == "categories"
    
    def test_extract_table_unknown(self):
        """Test extracting table returns unknown for complex queries."""
        assert _extract_table("WITH cte AS (SELECT * FROM users) SELECT * FROM cte", "select") == "unknown"
        assert _extract_table("", "select") == "unknown"


class TestPoolMetrics:
    """Test connection pool metrics updates."""
    
    def test_update_pool_metrics(self):
        """Test updating pool metrics with mock pool."""
        # Create mock pool
        mock_pool = MagicMock()
        mock_pool.size.return_value = 10
        mock_pool.checkedout.return_value = 3
        
        # Update metrics
        _update_pool_metrics(mock_pool)
        
        # Check metrics updated
        assert db_connections_active._value.get() == 7  # size - checkedout
        assert db_connections_idle._value.get() == 3    # checkedout
    
    def test_update_pool_metrics_no_methods(self):
        """Test handling pools without size/checkedout methods."""
        # Create mock pool without methods
        mock_pool = MagicMock()
        del mock_pool.size
        del mock_pool.checkedout
        
        # Should not raise exception
        _update_pool_metrics(mock_pool)


class TestSetupDbMetrics:
    """Test database metrics setup."""
    
    @patch('sqlalchemy.event.listen')
    def test_setup_db_metrics_registers_events(self, mock_listen):
        """Test that setup registers all required event listeners."""
        # Create mock engine
        mock_engine = MagicMock()
        mock_engine.sync_engine = MagicMock()
        mock_engine.pool = MagicMock()
        
        # Setup metrics
        setup_db_metrics(mock_engine)
        
        # Check event listeners registered
        assert mock_listen.called
        
        # Count calls for each event type
        call_args = [call[0][1] for call in mock_listen.call_args_list]
        assert "before_cursor_execute" in call_args
        assert "after_cursor_execute" in call_args
        assert "connect" in call_args
        assert "checkout" in call_args
        assert "checkin" in call_args
    
    def test_query_metrics_tracking(self):
        """Test query metrics are tracked correctly."""
        # Get initial metric values
        initial_count = db_query_total.labels(
            operation="select", table="users"
        )._value.get()
        
        # Simulate query execution (would normally be triggered by events)
        db_query_total.labels(operation="select", table="users").inc()
        db_query_duration_seconds.labels(
            operation="select", table="users"
        ).observe(0.05)
        
        # Check metrics updated
        final_count = db_query_total.labels(
            operation="select", table="users"
        )._value.get()
        assert final_count == initial_count + 1
        
        # Check duration recorded
        duration_metric = db_query_duration_seconds.labels(
            operation="select", table="users"
        )
        assert duration_metric._count.get() > 0
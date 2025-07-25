"""Database metrics collection using SQLAlchemy events."""
import time
from typing import Any

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool

from app.monitoring.logging_config import get_logger
from app.monitoring.metrics import (
    db_connections_active,
    db_connections_idle,
    db_query_duration_seconds,
    db_query_total,
)

logger = get_logger(__name__)


def setup_db_metrics(engine: Engine) -> None:
    """Set up database metrics collection using SQLAlchemy events.
    
    Args:
        engine: SQLAlchemy engine to instrument
    """
    # Track query execution
    @event.listens_for(engine.sync_engine, "before_cursor_execute", named=True)
    def before_cursor_execute(**kw: Any) -> None:
        """Record query start time."""
        conn = kw["conn"]
        conn.info["query_start_time"] = time.time()

    @event.listens_for(engine.sync_engine, "after_cursor_execute", named=True)
    def after_cursor_execute(**kw: Any) -> None:
        """Record query metrics."""
        conn = kw["conn"]
        statement = kw["statement"]

        # Calculate duration
        start_time = conn.info.pop("query_start_time", None)
        if start_time:
            duration = time.time() - start_time

            # Extract operation and table from SQL
            operation = _extract_operation(statement)
            table = _extract_table(statement, operation)

            # Record metrics
            db_query_total.labels(operation=operation, table=table).inc()
            db_query_duration_seconds.labels(operation=operation, table=table).observe(duration)

            # Log slow queries
            if duration > 1.0:  # Queries taking more than 1 second
                logger.warning(
                    "Slow query detected",
                    extra={
                        "operation": operation,
                        "table": table,
                        "duration": duration,
                        "query": statement[:200],  # First 200 chars
                    }
                )

    # Track connection pool metrics
    @event.listens_for(engine.pool, "connect")
    def on_connect(dbapi_conn: Any, connection_record: Any) -> None:
        """Track new connection creation."""
        _update_pool_metrics(engine.pool)

    @event.listens_for(engine.pool, "checkout")
    def on_checkout(dbapi_conn: Any, connection_record: Any, connection_proxy: Any) -> None:
        """Track connection checkout from pool."""
        _update_pool_metrics(engine.pool)

    @event.listens_for(engine.pool, "checkin")
    def on_checkin(dbapi_conn: Any, connection_record: Any) -> None:
        """Track connection checkin to pool."""
        _update_pool_metrics(engine.pool)

    logger.info("Database metrics collection configured")


def _extract_operation(statement: str) -> str:
    """Extract SQL operation from statement.
    
    Args:
        statement: SQL statement
        
    Returns:
        Operation type (select, insert, update, delete, other)
    """
    statement_lower = statement.lower().strip()

    if statement_lower.startswith("select"):
        return "select"
    elif statement_lower.startswith("insert"):
        return "insert"
    elif statement_lower.startswith("update"):
        return "update"
    elif statement_lower.startswith("delete"):
        return "delete"
    elif statement_lower.startswith("begin"):
        return "transaction"
    elif statement_lower.startswith("commit"):
        return "transaction"
    elif statement_lower.startswith("rollback"):
        return "transaction"
    else:
        return "other"


def _extract_table(statement: str, operation: str) -> str:
    """Extract table name from SQL statement.
    
    Args:
        statement: SQL statement
        operation: SQL operation type
        
    Returns:
        Table name or "unknown"
    """
    statement_lower = statement.lower()

    try:
        if operation == "select":
            # Extract from FROM clause
            from_idx = statement_lower.find(" from ")
            if from_idx > -1:
                rest = statement_lower[from_idx + 6:].strip()
                table = rest.split()[0].strip('"')
                return table

        elif operation == "insert":
            # Extract from INSERT INTO
            into_idx = statement_lower.find(" into ")
            if into_idx > -1:
                rest = statement_lower[into_idx + 6:].strip()
                table = rest.split()[0].strip('"')
                return table

        elif operation in ["update", "delete"]:
            # Extract from UPDATE/DELETE FROM
            parts = statement_lower.split()
            if len(parts) > 1:
                # Skip keywords
                for i, part in enumerate(parts[1:], 1):
                    if part not in ["from", "only"]:
                        return part.strip('"')

    except Exception:
        # Fallback for complex queries
        pass

    return "unknown"


def _update_pool_metrics(pool: Pool) -> None:
    """Update connection pool metrics.
    
    Args:
        pool: SQLAlchemy connection pool
    """
    try:
        # These attributes might not be available for all pool types
        db_connections_active.set(pool.size() - pool.checkedout())
        db_connections_idle.set(pool.checkedout())
    except AttributeError:
        # Some pool implementations don't have these methods
        pass

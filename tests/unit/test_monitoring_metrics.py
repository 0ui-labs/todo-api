"""Unit tests for monitoring metrics."""
import pytest
from prometheus_client import REGISTRY

from app.monitoring.metrics import (
    http_requests_total,
    http_request_duration_seconds,
    http_requests_in_progress,
    db_query_total,
    db_query_duration_seconds,
    cache_hits_total,
    cache_misses_total,
    cache_sets_total,
    cache_deletes_total,
    todos_created_total,
    todos_completed_total,
    todos_deleted_total,
    users_registered_total,
    users_login_total,
    rate_limit_exceeded_total,
    errors_total,
)


class TestPrometheusMetrics:
    """Test Prometheus metrics are properly registered and functional."""
    
    def test_http_metrics_registered(self):
        """Test HTTP metrics are registered in Prometheus registry."""
        # Check counters
        assert "http_requests_total" in REGISTRY._names_to_collectors
        assert "rate_limit_exceeded_total" in REGISTRY._names_to_collectors
        assert "errors_total" in REGISTRY._names_to_collectors
        
        # Check histogram
        assert "http_request_duration_seconds" in REGISTRY._names_to_collectors
        
        # Check gauge
        assert "http_requests_in_progress" in REGISTRY._names_to_collectors
    
    def test_database_metrics_registered(self):
        """Test database metrics are registered."""
        assert "db_query_total" in REGISTRY._names_to_collectors
        assert "db_query_duration_seconds" in REGISTRY._names_to_collectors
        assert "db_connections_active" in REGISTRY._names_to_collectors
        assert "db_connections_idle" in REGISTRY._names_to_collectors
    
    def test_cache_metrics_registered(self):
        """Test cache metrics are registered."""
        assert "cache_hits_total" in REGISTRY._names_to_collectors
        assert "cache_misses_total" in REGISTRY._names_to_collectors
        assert "cache_sets_total" in REGISTRY._names_to_collectors
        assert "cache_deletes_total" in REGISTRY._names_to_collectors
    
    def test_business_metrics_registered(self):
        """Test business metrics are registered."""
        assert "todos_created_total" in REGISTRY._names_to_collectors
        assert "todos_completed_total" in REGISTRY._names_to_collectors
        assert "todos_deleted_total" in REGISTRY._names_to_collectors
        assert "users_registered_total" in REGISTRY._names_to_collectors
        assert "users_login_total" in REGISTRY._names_to_collectors
    
    def test_http_request_counter_increment(self):
        """Test HTTP request counter can be incremented."""
        # Get initial value
        before = http_requests_total.labels(
            method="GET", endpoint="/test", status=200
        )._value.get()
        
        # Increment
        http_requests_total.labels(
            method="GET", endpoint="/test", status=200
        ).inc()
        
        # Check incremented
        after = http_requests_total.labels(
            method="GET", endpoint="/test", status=200
        )._value.get()
        
        assert after == before + 1
    
    def test_http_request_duration_observation(self):
        """Test HTTP request duration histogram."""
        # Record a duration
        http_request_duration_seconds.labels(
            method="POST", endpoint="/api/v1/todos"
        ).observe(0.123)
        
        # Get histogram data
        histogram = http_request_duration_seconds.labels(
            method="POST", endpoint="/api/v1/todos"
        )
        
        # Check count increased
        assert histogram._count.get() > 0
        # Check sum includes our observation
        assert histogram._sum.get() >= 0.123
    
    def test_gauge_inc_dec(self):
        """Test gauge increment and decrement."""
        # Get initial value
        initial = http_requests_in_progress._value.get()
        
        # Increment
        http_requests_in_progress.inc()
        assert http_requests_in_progress._value.get() == initial + 1
        
        # Decrement
        http_requests_in_progress.dec()
        assert http_requests_in_progress._value.get() == initial
    
    def test_cache_metrics_labels(self):
        """Test cache metrics with namespace labels."""
        # Increment different namespaces
        cache_hits_total.labels(namespace="todos").inc()
        cache_hits_total.labels(namespace="categories").inc()
        cache_misses_total.labels(namespace="todos").inc()
        
        # Check values are tracked separately
        todos_hits = cache_hits_total.labels(namespace="todos")._value.get()
        categories_hits = cache_hits_total.labels(namespace="categories")._value.get()
        
        assert todos_hits >= 1
        assert categories_hits >= 1
    
    def test_user_login_metrics_labels(self):
        """Test user login metrics with status labels."""
        # Track successful and failed logins
        users_login_total.labels(status="success").inc()
        users_login_total.labels(status="failure").inc()
        users_login_total.labels(status="failure").inc()
        
        # Check values
        success_count = users_login_total.labels(status="success")._value.get()
        failure_count = users_login_total.labels(status="failure")._value.get()
        
        assert success_count >= 1
        assert failure_count >= 2
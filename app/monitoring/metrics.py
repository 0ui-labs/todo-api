"""Prometheus metrics for the application."""
import asyncio
import time
from collections.abc import Callable
from functools import wraps

from prometheus_client import Counter, Gauge, Histogram, Info

# Application info
app_info = Info('app_info', 'Application information')
app_info.info({
    'version': '1.0.0',
    'name': 'todo-api'
})

# HTTP metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests in progress'
)

# Database metrics
db_query_total = Counter(
    'db_query_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

db_connections_active = Gauge(
    'db_connections_active',
    'Number of active database connections'
)

db_connections_idle = Gauge(
    'db_connections_idle',
    'Number of idle database connections'
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['namespace']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['namespace']
)

cache_sets_total = Counter(
    'cache_sets_total',
    'Total cache sets',
    ['namespace']
)

cache_deletes_total = Counter(
    'cache_deletes_total',
    'Total cache deletes',
    ['namespace']
)

# Business metrics
todos_created_total = Counter(
    'todos_created_total',
    'Total number of todos created'
)

todos_completed_total = Counter(
    'todos_completed_total',
    'Total number of todos completed'
)

todos_deleted_total = Counter(
    'todos_deleted_total',
    'Total number of todos deleted'
)

users_registered_total = Counter(
    'users_registered_total',
    'Total number of users registered'
)

users_login_total = Counter(
    'users_login_total',
    'Total number of user logins',
    ['status']  # success/failure
)

# Rate limiting metrics
rate_limit_exceeded_total = Counter(
    'rate_limit_exceeded_total',
    'Total number of rate limit exceeded events',
    ['endpoint']
)

# Error metrics
errors_total = Counter(
    'errors_total',
    'Total number of errors',
    ['type', 'endpoint']
)


def track_request_metrics(method: str, endpoint: str):
    """Decorator to track HTTP request metrics."""
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                http_requests_in_progress.inc()
                start_time = time.time()

                try:
                    response = await func(*args, **kwargs)
                    status = getattr(response, 'status_code', 200)
                    http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=status
                    ).inc()
                    return response
                except Exception as e:
                    http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=500
                    ).inc()
                    errors_total.labels(
                        type=type(e).__name__,
                        endpoint=endpoint
                    ).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    http_request_duration_seconds.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(duration)
                    http_requests_in_progress.dec()
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                http_requests_in_progress.inc()
                start_time = time.time()

                try:
                    response = func(*args, **kwargs)
                    status = getattr(response, 'status_code', 200)
                    http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=status
                    ).inc()
                    return response
                except Exception as e:
                    http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=500
                    ).inc()
                    errors_total.labels(
                        type=type(e).__name__,
                        endpoint=endpoint
                    ).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    http_request_duration_seconds.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(duration)
                    http_requests_in_progress.dec()
            return sync_wrapper
    return decorator

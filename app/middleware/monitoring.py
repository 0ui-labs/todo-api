"""Monitoring middleware for metrics collection."""
import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.monitoring.metrics import (
    errors_total,
    http_request_duration_seconds,
    http_requests_in_progress,
    http_requests_total,
    rate_limit_exceeded_total,
)


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and collect metrics."""
        # Skip metrics endpoint to avoid recursion
        if request.url.path == "/metrics":
            return await call_next(request)

        # Extract route pattern (e.g., /api/v1/todos/{todo_id})
        route = request.url.path
        if request.scope.get("route"):
            route = request.scope["route"].path

        # Track in-progress requests
        http_requests_in_progress.inc()

        # Start timing
        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Track request metrics
            http_requests_total.labels(
                method=request.method,
                endpoint=route,
                status=response.status_code
            ).inc()

            # Track rate limit exceeded
            if response.status_code == 429:
                rate_limit_exceeded_total.labels(endpoint=route).inc()

            return response

        except Exception as e:
            # Track errors
            http_requests_total.labels(
                method=request.method,
                endpoint=route,
                status=500
            ).inc()

            errors_total.labels(
                type=type(e).__name__,
                endpoint=route
            ).inc()

            raise

        finally:
            # Record duration
            duration = time.time() - start_time
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=route
            ).observe(duration)

            # Decrement in-progress counter
            http_requests_in_progress.dec()

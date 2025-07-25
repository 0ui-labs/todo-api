"""Unit tests for monitoring middleware."""
import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, Request, Response

from app.middleware.monitoring import MonitoringMiddleware
from app.monitoring.metrics import (
    errors_total,
    http_request_duration_seconds,
    http_requests_in_progress,
    http_requests_total,
    rate_limit_exceeded_total,
)


@pytest.fixture
def app():
    """Create test FastAPI app."""
    app = FastAPI()
    return app


@pytest.fixture
def monitoring_middleware(app):
    """Create monitoring middleware instance."""
    return MonitoringMiddleware(app)


class TestMonitoringMiddleware:
    """Test monitoring middleware functionality."""

    @pytest.mark.asyncio
    async def test_metrics_endpoint_skipped(self, monitoring_middleware):
        """Test that /metrics endpoint is not monitored to avoid recursion."""
        # Create mock request for /metrics
        request = MagicMock(spec=Request)
        request.url.path = "/metrics"

        # Create mock call_next that returns a response
        call_next = AsyncMock(return_value=Response(content="metrics"))

        # Process request
        response = await monitoring_middleware.dispatch(request, call_next)

        # Verify call_next was called
        call_next.assert_called_once_with(request)
        assert response.body == b"metrics"

    @pytest.mark.asyncio
    async def test_successful_request_metrics(self, monitoring_middleware):
        """Test metrics collection for successful requests."""
        # Get initial metric values
        initial_total = http_requests_total.labels(
            method="GET", endpoint="/api/v1/todos", status=200
        )._value.get()
        initial_in_progress = http_requests_in_progress._value.get()

        # Create mock request
        request = MagicMock(spec=Request)
        request.url.path = "/api/v1/todos"
        request.method = "GET"
        request.scope = {"route": MagicMock(path="/api/v1/todos")}

        # Create mock response
        response = Response(content="success", status_code=200)
        call_next = AsyncMock(return_value=response)

        # Process request
        result = await monitoring_middleware.dispatch(request, call_next)

        # Check response
        assert result.status_code == 200

        # Check metrics updated
        final_total = http_requests_total.labels(
            method="GET", endpoint="/api/v1/todos", status=200
        )._value.get()
        assert final_total == initial_total + 1

        # Check in-progress gauge returned to initial value
        assert http_requests_in_progress._value.get() == initial_in_progress

        # Check duration recorded
        duration_metric = http_request_duration_seconds.labels(
            method="GET", endpoint="/api/v1/todos"
        )
        assert duration_metric._count.get() > 0

    @pytest.mark.asyncio
    async def test_rate_limit_metrics(self, monitoring_middleware):
        """Test rate limit exceeded metrics."""
        # Get initial value
        initial_count = rate_limit_exceeded_total.labels(
            endpoint="/api/v1/todos"
        )._value.get()

        # Create mock request
        request = MagicMock(spec=Request)
        request.url.path = "/api/v1/todos"
        request.method = "POST"
        request.scope = {"route": MagicMock(path="/api/v1/todos")}

        # Create 429 response
        response = Response(content="Rate limit exceeded", status_code=429)
        call_next = AsyncMock(return_value=response)

        # Process request
        await monitoring_middleware.dispatch(request, call_next)

        # Check rate limit metric incremented
        final_count = rate_limit_exceeded_total.labels(
            endpoint="/api/v1/todos"
        )._value.get()
        assert final_count == initial_count + 1

    @pytest.mark.asyncio
    async def test_error_metrics(self, monitoring_middleware):
        """Test error metrics collection."""
        # Get initial values
        initial_errors = errors_total.labels(
            type="ValueError", endpoint="/api/v1/todos"
        )._value.get()
        initial_requests = http_requests_total.labels(
            method="POST", endpoint="/api/v1/todos", status=500
        )._value.get()

        # Create mock request
        request = MagicMock(spec=Request)
        request.url.path = "/api/v1/todos"
        request.method = "POST"
        request.scope = {"route": MagicMock(path="/api/v1/todos")}

        # Make call_next raise an exception
        call_next = AsyncMock(side_effect=ValueError("Test error"))

        # Process request and expect exception
        with pytest.raises(ValueError):
            await monitoring_middleware.dispatch(request, call_next)

        # Check error metrics updated
        final_errors = errors_total.labels(
            type="ValueError", endpoint="/api/v1/todos"
        )._value.get()
        assert final_errors == initial_errors + 1

        # Check request counted as 500
        final_requests = http_requests_total.labels(
            method="POST", endpoint="/api/v1/todos", status=500
        )._value.get()
        assert final_requests == initial_requests + 1

    @pytest.mark.asyncio
    async def test_route_extraction(self, monitoring_middleware):
        """Test route pattern extraction from request."""
        # Test with route in scope
        request = MagicMock(spec=Request)
        request.url.path = "/api/v1/todos/123"
        request.method = "GET"
        request.scope = {"route": MagicMock(path="/api/v1/todos/{todo_id}")}

        response = Response(content="success", status_code=200)
        call_next = AsyncMock(return_value=response)

        # Process request
        await monitoring_middleware.dispatch(request, call_next)

        # Check metric uses route pattern, not actual path
        metric_value = http_requests_total.labels(
            method="GET",
            endpoint="/api/v1/todos/{todo_id}",
            status=200
        )._value.get()
        assert metric_value > 0

    @pytest.mark.asyncio
    async def test_in_progress_gauge_tracking(self, monitoring_middleware):
        """Test in-progress requests gauge increments and decrements."""
        initial_value = http_requests_in_progress._value.get()

        # Create request
        request = MagicMock(spec=Request)
        request.url.path = "/api/v1/test"
        request.method = "GET"
        request.scope = {}

        # Create a slow call_next to check gauge during request
        gauge_during_request = None

        async def slow_call_next(req):
            nonlocal gauge_during_request
            gauge_during_request = http_requests_in_progress._value.get()
            await asyncio.sleep(0.1)  # Simulate slow request
            return Response(content="success")

        # Process request
        await monitoring_middleware.dispatch(request, slow_call_next)

        # Check gauge was incremented during request
        assert gauge_during_request == initial_value + 1

        # Check gauge returned to initial value after request
        assert http_requests_in_progress._value.get() == initial_value

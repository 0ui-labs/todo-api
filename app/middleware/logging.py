"""Logging middleware for request/response tracking."""
import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses with structured logging."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request and add logging."""
        from app.monitoring.logging_config import (
            request_id_context,
            span_id_context,
            trace_id_context,
            user_id_context,
        )
        from app.monitoring.tracing import get_span_id, get_trace_id

        # Generate request ID
        request_id = str(uuid.uuid4())

        # Add request ID to request state
        request.state.request_id = request_id

        # Set context variables for structured logging
        request_id_context.set(request_id)

        # Set trace and span IDs if available
        trace_id = get_trace_id()
        if trace_id:
            trace_id_context.set(trace_id)

        span_id = get_span_id()
        if span_id:
            span_id_context.set(span_id)

        # Try to get user ID from request if authenticated
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            user_id_context.set(str(user_id))

        # Log request with structured data
        start_time = time.time()
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate process time
            process_time = time.time() - start_time

            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            # Log response with structured data
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                    "response_size": response.headers.get("content-length", 0),
                }
            )

            return response

        except Exception as e:
            # Log error with structured data
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "process_time": process_time,
                },
                exc_info=True
            )
            raise
        finally:
            # Clear context variables
            request_id_context.set(None)
            user_id_context.set(None)
            trace_id_context.set(None)
            span_id_context.set(None)

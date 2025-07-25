"""Middleware package for the Todo API."""
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.monitoring import MonitoringMiddleware
from app.middleware.rate_limit import limiter, setup_rate_limiting
from app.middleware.registry import MiddlewareRegistry, create_middleware_registry
from app.middleware.request import RequestSizeLimitMiddleware, RequestTimeoutMiddleware
from app.middleware.security import SecurityHeadersMiddleware

__all__ = [
    "ErrorHandlerMiddleware",
    "LoggingMiddleware",
    "MonitoringMiddleware",
    "limiter",
    "setup_rate_limiting",
    "MiddlewareRegistry",
    "create_middleware_registry",
    "RequestSizeLimitMiddleware",
    "RequestTimeoutMiddleware",
    "SecurityHeadersMiddleware",
]
"""Middleware registry and configuration."""
from typing import Type, Optional
from dataclasses import dataclass

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.middleware.request import RequestSizeLimitMiddleware, RequestTimeoutMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.monitoring import MonitoringMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware


@dataclass
class MiddlewareConfig:
    """Configuration for a middleware component."""
    middleware_class: Type[BaseHTTPMiddleware]
    enabled: bool = True
    config: dict = None
    order: int = 0  # Lower numbers execute first
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


class MiddlewareRegistry:
    """Central registry for application middleware."""
    
    def __init__(self):
        self.middleware_configs = []
    
    def register(self, config: MiddlewareConfig):
        """Register a middleware configuration."""
        self.middleware_configs.append(config)
        # Sort by order
        self.middleware_configs.sort(key=lambda x: x.order)
    
    def apply_to_app(self, app: FastAPI):
        """Apply all registered middleware to the app."""
        # Apply in reverse order (last registered executes first)
        for config in reversed(self.middleware_configs):
            if config.enabled and settings.middleware_enabled:
                app.add_middleware(
                    config.middleware_class,
                    **config.config
                )


def create_middleware_registry() -> MiddlewareRegistry:
    """Create and configure the middleware registry."""
    registry = MiddlewareRegistry()
    
    # Error handling (should be outermost)
    registry.register(MiddlewareConfig(
        middleware_class=ErrorHandlerMiddleware,
        order=10,
        enabled=True
    ))
    
    # Monitoring
    registry.register(MiddlewareConfig(
        middleware_class=MonitoringMiddleware,
        order=20,
        enabled=settings.metrics_collection_enabled
    ))
    
    # Security headers
    registry.register(MiddlewareConfig(
        middleware_class=SecurityHeadersMiddleware,
        order=30,
        enabled=settings.security_headers_enabled
    ))
    
    # Request size limiting
    registry.register(MiddlewareConfig(
        middleware_class=RequestSizeLimitMiddleware,
        order=40,
        enabled=True,
        config={
            "max_size": settings.max_request_size,
            "error_message": settings.request_size_error_message,
            "include_max_size_in_error": True
        }
    ))
    
    # Request logging
    registry.register(MiddlewareConfig(
        middleware_class=LoggingMiddleware,
        order=50,
        enabled=settings.request_logging_enabled
    ))
    
    return registry
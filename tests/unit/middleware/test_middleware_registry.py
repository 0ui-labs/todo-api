"""Tests for middleware registry."""
from unittest.mock import Mock, patch

from fastapi import FastAPI

from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.monitoring import MonitoringMiddleware
from app.middleware.registry import (
    MiddlewareConfig,
    MiddlewareRegistry,
    create_middleware_registry,
)
from app.middleware.request import RequestSizeLimitMiddleware
from app.middleware.security import SecurityHeadersMiddleware


class TestMiddlewareConfig:
    """Test cases for MiddlewareConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware
        )
        assert config.middleware_class == RequestSizeLimitMiddleware
        assert config.enabled is True
        assert config.config == {}
        assert config.order == 0

    def test_custom_config(self):
        """Test custom configuration values."""
        custom_config = {"max_size": 1024}
        config = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware,
            enabled=False,
            config=custom_config,
            order=10
        )
        assert config.enabled is False
        assert config.config == custom_config
        assert config.order == 10


class TestMiddlewareRegistry:
    """Test cases for MiddlewareRegistry."""

    def test_register_middleware(self):
        """Test registering middleware configurations."""
        registry = MiddlewareRegistry()

        config1 = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware,
            order=20
        )
        config2 = MiddlewareConfig(
            middleware_class=SecurityHeadersMiddleware,
            order=10
        )

        registry.register(config1)
        registry.register(config2)

        assert len(registry.middleware_configs) == 2
        # Should be sorted by order
        assert registry.middleware_configs[0].middleware_class == SecurityHeadersMiddleware
        assert registry.middleware_configs[1].middleware_class == RequestSizeLimitMiddleware

    @patch('app.config.settings')
    def test_apply_to_app_with_middleware_enabled(self, mock_settings):
        """Test applying middleware when enabled."""
        mock_settings.middleware_enabled = True

        app = FastAPI()
        mock_add_middleware = Mock()
        app.add_middleware = mock_add_middleware

        registry = MiddlewareRegistry()
        config = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware,
            config={"max_size": 1024}
        )
        registry.register(config)

        registry.apply_to_app(app)

        mock_add_middleware.assert_called_once_with(
            RequestSizeLimitMiddleware,
            max_size=1024
        )

    @patch('app.config.settings')
    def test_apply_to_app_with_middleware_disabled(self, mock_settings):
        """Test that middleware is not applied when globally disabled."""
        mock_settings.middleware_enabled = False

        app = FastAPI()
        mock_add_middleware = Mock()
        app.add_middleware = mock_add_middleware

        registry = MiddlewareRegistry()
        config = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware
        )
        registry.register(config)

        registry.apply_to_app(app)

        mock_add_middleware.assert_not_called()

    @patch('app.config.settings')
    def test_apply_to_app_with_individual_middleware_disabled(self, mock_settings):
        """Test that individually disabled middleware is not applied."""
        mock_settings.middleware_enabled = True

        app = FastAPI()
        mock_add_middleware = Mock()
        app.add_middleware = mock_add_middleware

        registry = MiddlewareRegistry()
        config = MiddlewareConfig(
            middleware_class=RequestSizeLimitMiddleware,
            enabled=False
        )
        registry.register(config)

        registry.apply_to_app(app)

        mock_add_middleware.assert_not_called()

    @patch('app.config.settings')
    def test_apply_to_app_reverse_order(self, mock_settings):
        """Test that middleware is applied in reverse order."""
        mock_settings.middleware_enabled = True

        app = FastAPI()
        middleware_calls = []

        def mock_add_middleware(middleware_class, **kwargs):
            middleware_calls.append(middleware_class)

        app.add_middleware = mock_add_middleware

        registry = MiddlewareRegistry()
        registry.register(MiddlewareConfig(
            middleware_class=ErrorHandlerMiddleware,
            order=10
        ))
        registry.register(MiddlewareConfig(
            middleware_class=MonitoringMiddleware,
            order=20
        ))
        registry.register(MiddlewareConfig(
            middleware_class=SecurityHeadersMiddleware,
            order=30
        ))

        registry.apply_to_app(app)

        # Should be applied in reverse order
        assert middleware_calls == [
            SecurityHeadersMiddleware,
            MonitoringMiddleware,
            ErrorHandlerMiddleware
        ]


class TestCreateMiddlewareRegistry:
    """Test cases for create_middleware_registry factory function."""

    @patch('app.config.settings')
    def test_create_middleware_registry(self, mock_settings):
        """Test creating a configured middleware registry."""
        # Setup mock settings
        mock_settings.metrics_collection_enabled = True
        mock_settings.security_headers_enabled = True
        mock_settings.max_request_size = 10485760  # 10MB
        mock_settings.request_size_error_message = "Request too large"
        mock_settings.request_logging_enabled = True

        registry = create_middleware_registry()

        assert isinstance(registry, MiddlewareRegistry)
        assert len(registry.middleware_configs) == 5

        # Check order
        orders = [config.order for config in registry.middleware_configs]
        assert orders == sorted(orders)  # Should be sorted

        # Check specific configurations
        error_handler_config = next(
            c for c in registry.middleware_configs
            if c.middleware_class == ErrorHandlerMiddleware
        )
        assert error_handler_config.order == 10
        assert error_handler_config.enabled is True

        request_size_config = next(
            c for c in registry.middleware_configs
            if c.middleware_class == RequestSizeLimitMiddleware
        )
        assert request_size_config.order == 40
        assert request_size_config.config["max_size"] == 10485760
        assert request_size_config.config["error_message"] == "Request too large"
        assert request_size_config.config["include_max_size_in_error"] is True

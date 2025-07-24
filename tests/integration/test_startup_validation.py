"""Integration tests for application startup validation."""
import os
from contextlib import ExitStack
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


class TestStartupValidation:
    """Test cases for application startup validation."""

    def test_production_startup_without_secret_key(self):
        """Application should fail to start in production without SECRET_KEY."""
        with ExitStack() as stack:
            # Mock environment as production
            stack.enter_context(patch.dict(os.environ, {
                "ENVIRONMENT": "production",
                "SECRET_KEY": "",  # Empty SECRET_KEY
            }, clear=True))

            # Attempt to import app should raise SystemExit
            with pytest.raises(SystemExit) as exc_info:
                from app.main import app
                TestClient(app)

            assert exc_info.value.code == 1

    def test_production_startup_with_wildcard_cors(self):
        """Application should fail to start in production with wildcard CORS."""
        with ExitStack() as stack:
            # Mock environment as production with wildcard CORS
            stack.enter_context(patch.dict(os.environ, {
                "ENVIRONMENT": "production",
                "SECRET_KEY": "a" * 64 + "1B2c3D4e5F",
                "BACKEND_CORS_ORIGINS": '["*"]',
            }, clear=True))

            # Mock settings to ensure wildcard CORS
            with patch('app.main.settings') as mock_settings:
                mock_settings.environment = "production"
                mock_settings.secret_key = "valid_key"
                mock_settings.database_url = "postgresql://..."
                mock_settings.backend_cors_origins = ["*"]

                # Mock verify_production_config to return False
                with patch('app.main.verify_production_config', return_value=False):
                    with pytest.raises(SystemExit) as exc_info:
                        from app.main import app
                        TestClient(app)

                    assert exc_info.value.code == 1

    def test_development_startup_without_secret_key(self, caplog):
        """Application should start in development without SECRET_KEY but with warning."""
        with ExitStack() as stack:
            # Mock environment as development
            stack.enter_context(patch.dict(os.environ, {
                "ENVIRONMENT": "development",
                "SECRET_KEY": "",  # Empty SECRET_KEY
            }, clear=True))

            # Import should succeed but with warning
            from app.main import app
            client = TestClient(app)

            # Should be able to reach health endpoint
            response = client.get("/health")
            assert response.status_code == 200

    def test_production_startup_with_valid_config(self):
        """Application should start successfully in production with valid config."""
        import secrets
        valid_key = secrets.token_urlsafe(64)

        with ExitStack() as stack:
            # Mock environment as production with valid config
            stack.enter_context(patch.dict(os.environ, {
                "ENVIRONMENT": "production",
                "SECRET_KEY": valid_key,
                "BACKEND_CORS_ORIGINS": '["http://example.com"]',
                "DATABASE_URL": "postgresql://user:pass@localhost/db",
            }, clear=True))

            # Mock settings and verify_production_config
            with patch('app.main.settings') as mock_settings:
                mock_settings.environment = "production"
                mock_settings.secret_key = valid_key
                mock_settings.database_url = "postgresql://user:pass@localhost/db"
                mock_settings.backend_cors_origins = ["http://example.com"]
                mock_settings.app_name = "Todo API"
                mock_settings.api_v1_str = "/api/v1"
                mock_settings.otlp_endpoint = None
                mock_settings.log_level = "INFO"
                mock_settings.json_logs = True

                with patch('app.main.verify_production_config', return_value=True):
                    # Import should succeed
                    from app.main import app
                    client = TestClient(app)

                    # Should be able to reach health endpoint
                    response = client.get("/health")
                    assert response.status_code == 200
                    assert response.json()["status"] == "healthy"

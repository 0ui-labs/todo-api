"""Unit tests for configuration security validation."""
import os
from unittest.mock import patch

import pytest
from pydantic import SecretStr, ValidationError

from app.config import Settings


class TestSecretKeyValidation:
    """Test cases for SECRET_KEY validation."""

    def test_production_requires_secret_key(self):
        """Production must fail without SECRET_KEY when set via environment."""
        # The field validator checks os.getenv, not the instance field
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                Settings(environment="production", secret_key=None)
            
            assert "SECRET_KEY is required in production" in str(exc_info.value)

    def test_development_generates_warning(self, caplog):
        """Development should warn but continue."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
            settings = Settings(environment="development", secret_key=None)
            assert settings.secret_key is not None
            assert "No SECRET_KEY set - generating temporary key" in caplog.text

    def test_secret_key_minimum_length(self):
        """SECRET_KEY must be at least 64 characters."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(secret_key=SecretStr("short_key"))

        errors = exc_info.value.errors()
        assert any("at least 64 characters long" in str(error) for error in errors)

    def test_secret_key_weak_patterns(self):
        """SECRET_KEY must not contain weak patterns."""
        weak_keys = [
            "a" * 64,  # Only letters
            "1" * 64,  # Only numbers
            "x" * 64,  # Repeating characters
            "secretsecretsecretsecretsecretsecretsecretsecretsecretsecret123",  # Contains 'secret'
            "passwordpasswordpasswordpasswordpasswordpasswordpasswordpass123",  # Contains 'password'
        ]

        for weak_key in weak_keys:
            with pytest.raises(ValidationError) as exc_info:
                Settings(secret_key=SecretStr(weak_key))

            # Check for either length or pattern error (length is checked first)
            error_str = str(exc_info.value)
            assert ("weak patterns" in error_str or "at least 64 characters" in error_str)

    def test_valid_secret_key(self):
        """Valid SECRET_KEY should pass validation."""
        import secrets
        valid_key = secrets.token_urlsafe(64)
        settings = Settings(secret_key=SecretStr(valid_key))
        assert settings.secret_key.get_secret_value() == valid_key

    def test_environment_default_is_development(self):
        """Default environment should be development."""
        settings = Settings(secret_key=SecretStr("a" * 64 + "1B2c3D4e5F"))
        assert settings.environment == "development"

    def test_production_with_valid_key(self):
        """Production with valid key should work."""
        import secrets
        valid_key = secrets.token_urlsafe(64)
        settings = Settings(
            environment="production",
            secret_key=SecretStr(valid_key)
        )
        assert settings.environment == "production"
        assert settings.secret_key.get_secret_value() == valid_key


class TestProductionConfigValidation:
    """Test cases for production configuration validation."""

    def test_verify_production_config_missing_secret(self):
        """Production config should fail with missing SECRET_KEY."""
        from app.main import verify_production_config

        with patch('app.main.settings') as mock_settings:
            mock_settings.secret_key = None
            mock_settings.database_url = "postgresql://..."
            mock_settings.backend_cors_origins = ["http://example.com"]

            assert verify_production_config() is False

    def test_verify_production_config_wildcard_cors(self):
        """Production config should fail with wildcard CORS."""
        from app.main import verify_production_config

        with patch('app.main.settings') as mock_settings:
            mock_settings.secret_key = SecretStr("valid_key_64_chars" * 4)
            mock_settings.database_url = "postgresql://..."
            mock_settings.backend_cors_origins = ["*"]

            assert verify_production_config() is False

    def test_verify_production_config_valid(self):
        """Production config should pass with all valid settings."""
        from app.main import verify_production_config

        with patch('app.main.settings') as mock_settings:
            mock_settings.secret_key = SecretStr("valid_key_64_chars" * 4)
            mock_settings.database_url = "postgresql://..."
            mock_settings.backend_cors_origins = ["http://example.com"]

            assert verify_production_config() is True

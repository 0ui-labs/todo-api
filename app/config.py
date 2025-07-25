"""Configuration settings for the Todo API."""

import logging
import os
import re
import secrets

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    @model_validator(mode='after')
    def validate_secret_key_requirement(self) -> 'Settings':
        """Ensure SECRET_KEY is set in production."""
        if self.environment == "production":
            if not self.secret_key:
                raise ValueError(
                    "SECRET_KEY is required in production environment. "
                    "Set it via environment variable."
                )
        return self

    # Application settings
    app_name: str = "Todo API"
    debug: bool = False
    api_v1_str: str = "/api/v1"

    # Database settings - component-based configuration
    database_user: str = Field(default="postgres")
    database_password: SecretStr = Field(default=SecretStr("postgres"))
    database_name: str = Field(default="todo_db")
    database_host: str = Field(default="localhost")
    database_port: int = Field(default=5432)
    database_echo: bool = False
    database_url_override: str | None = Field(default=None)

    # Redis settings - component-based configuration
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_rate_limit_db: int = Field(default=1)
    redis_url_override: str | None = Field(default=None)

    # Environment settings
    environment: str = Field(default="development")
    require_secure_key: bool = Field(default=True)

    # Security settings
    secret_key: SecretStr | None = Field(
        default=None,
        description="JWT secret key - REQUIRED in production"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS settings
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 100
    rate_limit_per_hour: int = 1000
    
    # Endpoint-specific limits (non-tier)
    rate_limit_auth_register: str = "10/hour"
    rate_limit_auth_login: str = "5/minute"



    # Monitoring and observability settings
    otlp_endpoint: str | None = Field(
        default=None, description="OpenTelemetry collector endpoint"
    )
    json_logs: bool = Field(default=True, description="Enable JSON structured logging")
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("secret_key", mode="after")
    @classmethod
    def validate_secret_key_strength(cls, v: SecretStr | None) -> SecretStr:
        """Enhanced validation with detailed feedback."""
        if not v:
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError("SECRET_KEY is required in production")
            # Development fallback
            logger.warning(
                "No SECRET_KEY set - generating temporary key for development. "
                "This is NOT secure for production!"
            )
            return SecretStr(secrets.token_urlsafe(64))

        secret = v.get_secret_value()

        # Check minimum length (OWASP recommendation)
        if len(secret) < 64:
            raise ValueError("JWT secret key must be at least 64 characters long")

        # Check for weak patterns
        weak_patterns = [
            r"^[a-zA-Z]+$",  # Only letters
            r"^[0-9]+$",  # Only numbers
            r"^(.)\1+$",  # Repeating characters
            r"(secret|password|test|demo|example)",  # Insecure keywords
        ]

        for pattern in weak_patterns:
            if re.search(pattern, secret, re.IGNORECASE):
                raise ValueError(
                    "JWT secret key contains weak patterns. "
                    "Use a cryptographically secure random string."
                )

        return v

    @staticmethod
    def generate_secure_key(length: int = 64) -> str:
        """Generate a cryptographically secure random key."""
        return secrets.token_urlsafe(length)

    @property
    def database_url(self) -> str:
        """Construct database URL from components or use provided URL."""
        # If explicitly set DATABASE_URL is provided, use it
        if self.database_url_override:
            return self.database_url_override

        # Otherwise construct from components
        password = self.database_password.get_secret_value()
        return f"postgresql+asyncpg://{self.database_user}:{password}@{self.database_host}:{self.database_port}/{self.database_name}"

    @property
    def redis_url(self) -> str:
        """Construct Redis URL from components or use provided URL."""
        # If explicitly set REDIS_URL is provided, use it
        if self.redis_url_override:
            return self.redis_url_override

        # Otherwise construct from components
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def sync_database_url(self) -> str:
        """Get synchronous database URL for Alembic migrations."""
        return self.database_url.replace("+asyncpg", "")


settings = Settings()

"""Configuration settings for the Todo API."""

import re
import secrets

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

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

    # Security settings
    secret_key: SecretStr = Field(
        default_factory=lambda: SecretStr(secrets.token_urlsafe(64)),
        description="JWT secret key - MUST be set in production via env variable",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS settings
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Rate limiting
    rate_limit_per_minute: int = 100
    rate_limit_per_hour: int = 1000

    # Advanced rate limiting settings
    rate_limit_burst_size: int = 10  # Allow burst of requests
    rate_limit_strategy: str = "moving-window"  # moving-window or fixed-window
    rate_limit_key_prefix: str = "todo_api"  # Redis key prefix
    rate_limit_auth_per_minute: int = 5
    rate_limit_auth_per_hour: int = 20

    @field_validator("secret_key", mode="after")
    @classmethod
    def validate_secret_key(cls, v: SecretStr) -> SecretStr:
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

"""
Environment-based rate limit configuration.

This module allows rate limits to be configured via environment variables,
making it easy to adjust limits without code changes.
"""

import os


class EnvRateLimitConfig:
    """Load rate limit configuration from environment variables."""

    # Environment variable prefix
    PREFIX = "RATE_LIMIT_"

    @classmethod
    def get_limit(cls, category: str, operation: str, default: str) -> str:
        """
        Get rate limit from environment or use default.
        
        Environment variable format: RATE_LIMIT_{CATEGORY}_{OPERATION}
        Example: RATE_LIMIT_AUTH_LOGIN=10/minute
        
        Args:
            category: Category name (e.g., "AUTH", "TODO", "CATEGORY")
            operation: Operation name (e.g., "LOGIN", "CREATE", "LIST")
            default: Default limit if env var not set
            
        Returns:
            Rate limit string (e.g., "10/minute")
        """
        env_var = f"{cls.PREFIX}{category.upper()}_{operation.upper()}"
        return os.getenv(env_var, default)

    @classmethod
    def get_tier_limits(cls, category: str, operation: str) -> dict[str, str] | None:
        """
        Get tier-specific limits from environment.
        
        Environment variable format: RATE_LIMIT_{CATEGORY}_{OPERATION}_{TIER}
        Example: RATE_LIMIT_TODO_CREATE_PREMIUM=100/minute
        
        Args:
            category: Category name
            operation: Operation name
            
        Returns:
            Dict of tier limits or None if no tier limits defined
        """
        tiers = ["BASIC", "PREMIUM", "ADMIN"]
        tier_limits = {}

        for tier in tiers:
            env_var = f"{cls.PREFIX}{category.upper()}_{operation.upper()}_{tier}"
            limit = os.getenv(env_var)
            if limit:
                tier_limits[tier.lower()] = limit

        return tier_limits if tier_limits else None

    @classmethod
    def get_burst_config(cls) -> dict[str, int]:
        """Get burst configuration from environment."""
        return {
            "size": int(os.getenv("RATE_LIMIT_BURST_SIZE", "10")),
            "refill_rate": int(os.getenv("RATE_LIMIT_BURST_REFILL_RATE", "1")),
            "refill_period": int(os.getenv("RATE_LIMIT_BURST_REFILL_PERIOD", "1")),
        }

    @classmethod
    def is_enabled(cls) -> bool:
        """Check if rate limiting is enabled."""
        return os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"

    @classmethod
    def get_strategy(cls) -> str:
        """Get rate limiting strategy."""
        return os.getenv("RATE_LIMIT_STRATEGY", "moving-window")

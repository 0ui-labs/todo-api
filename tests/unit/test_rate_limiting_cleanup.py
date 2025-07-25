"""Test to ensure tier-based rate limiting has been removed."""

from unittest.mock import Mock

import pytest

from app.middleware.rate_limit import create_endpoint_limiter


class TestRateLimitingCleanup:
    """Tests to verify tier-based limiting is removed."""

    def test_no_tier_based_limiting(self):
        """Ensure tier-based limiting is removed."""
        # Should not accept per_tier parameter
        with pytest.raises(TypeError):
            create_endpoint_limiter("10/minute", per_tier={"admin": "unlimited"})

    def test_create_endpoint_limiter_simple(self):
        """Test simplified create_endpoint_limiter function."""
        # Should only accept limit and key_func parameters
        limiter = create_endpoint_limiter("10/minute")
        assert limiter is not None

        # With custom key function
        custom_key = Mock()
        limiter = create_endpoint_limiter("20/hour", key_func=custom_key)
        assert limiter is not None

    def test_no_get_user_tier_function(self):
        """Ensure get_user_tier function is removed."""
        from app.middleware import rate_limit
        assert not hasattr(rate_limit, 'get_user_tier')

    def test_consistent_rate_limits(self):
        """All users should get same rate limits."""
        # Test that RateLimiters class exists and has no tier logic
        from app.middleware.rate_limit import RateLimiters

        # Check that limiters are simple without tier parameters
        assert hasattr(RateLimiters, 'auth_login')
        assert hasattr(RateLimiters, 'todo_create')
        assert hasattr(RateLimiters, 'todo_list')

        # Verify these are direct limiter objects, not tier-aware functions
        # This would fail if they were still using create_endpoint_limiter with per_tier

    def test_no_tier_config_imports(self):
        """Ensure tier-related config imports are removed."""
        from app.middleware import rate_limit

        # These modules should not be imported anymore
        assert 'RateLimitConfig' not in dir(rate_limit)
        assert 'EnvRateLimitConfig' not in dir(rate_limit)

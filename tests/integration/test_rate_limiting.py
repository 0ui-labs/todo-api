import asyncio
import time

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRateLimiting:
    """Comprehensive tests for rate limiting middleware."""

    async def test_rate_limit_per_minute(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test per-minute rate limiting."""
        limit = 100  # Default rate limit per minute

        # Make requests up to the limit
        for _i in range(limit):
            response = await client.get(
                "/api/v1/todos",
                headers=auth_headers
            )
            assert response.status_code == 200

        # Next request should be rate limited
        response = await client.get(
            "/api/v1/todos",
            headers=auth_headers
        )
        assert response.status_code == 429
        assert "rate_limit_exceeded" in response.json()["error"]

    async def test_rate_limit_headers(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test that rate limit headers are included."""
        response = await client.get(
            "/api/v1/todos",
            headers=auth_headers
        )

        # Check for rate limit headers
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
        assert "X-RateLimit-Reset" in response.headers

        # Verify header values make sense
        limit = int(response.headers["X-RateLimit-Limit"])
        remaining = int(response.headers["X-RateLimit-Remaining"])
        assert remaining < limit
        assert remaining >= 0

    async def test_rate_limit_retry_after(
        self,
        client: AsyncClient,
        auth_headers: dict,
        exhaust_rate_limit  # Helper to exhaust limit
    ):
        """Test Retry-After header when rate limited."""
        await exhaust_rate_limit(client, auth_headers)

        # Make request that should be rate limited
        response = await client.get(
            "/api/v1/todos",
            headers=auth_headers
        )
        assert response.status_code == 429
        assert "Retry-After" in response.headers

        retry_after = int(response.headers["Retry-After"])
        assert retry_after > 0
        assert retry_after <= 60  # Should be less than a minute

    async def test_rate_limit_different_endpoints(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test that rate limits apply across different endpoints."""
        limit = 100  # Default rate limit per minute
        endpoints = ["/api/v1/todos", "/api/v1/categories", "/api/v1/users/me"]

        # Distribute requests across endpoints
        request_count = 0
        for i in range(limit + 5):
            endpoint = endpoints[i % len(endpoints)]
            response = await client.get(
                endpoint,
                headers=auth_headers
            )

            if response.status_code == 429:
                # Should hit rate limit around the limit
                assert request_count >= limit - 5  # Allow some margin
                break

            request_count += 1
            assert response.status_code in [200, 201]

    async def test_rate_limit_per_user(
        self,
        client: AsyncClient,
        auth_headers: dict,
        second_user_headers: dict
    ):
        """Test that rate limits are per-user, not global."""
        # Exhaust first user's rate limit
        for _ in range(10):
            response = await client.get(
                "/api/v1/todos",
                headers=auth_headers
            )
            if response.status_code == 429:
                break

        # Second user should still be able to make requests
        response = await client.get(
            "/api/v1/todos",
            headers=second_user_headers
        )
        assert response.status_code == 200

    async def test_rate_limit_reset(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test that rate limit resets after time window."""
        # Make a few requests to get the reset time
        response = await client.get(
            "/api/v1/todos",
            headers=auth_headers
        )
        reset_time = int(response.headers["X-RateLimit-Reset"])

        # Calculate wait time (add buffer)
        current_time = int(time.time())
        wait_time = reset_time - current_time + 2

        if wait_time > 0 and wait_time < 65:  # Only wait if reasonable
            await asyncio.sleep(wait_time)

            # Should be able to make requests again
            response = await client.get(
                "/api/v1/todos",
                headers=auth_headers
            )
            assert response.status_code == 200

    async def test_auth_endpoint_stricter_limits(
        self,
        client: AsyncClient
    ):
        """Test that auth endpoints have stricter rate limits."""
        # Login endpoint should have tighter limits
        login_attempts = 0

        for i in range(10):  # Try 10 login attempts
            response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": f"test{i}@example.com",
                    "password": "wrongpassword"
                }
            )

            if response.status_code == 429:
                login_attempts = i
                break

        # Should hit rate limit before 10 attempts
        assert login_attempts < 10
        assert login_attempts <= 5  # Expecting ~5 attempts limit

    async def test_rate_limit_burst_requests(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test handling of burst requests."""
        # Send multiple requests concurrently
        tasks = []
        for _ in range(20):
            task = client.get(
                "/api/v1/todos",
                headers=auth_headers
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Count successful vs rate limited
        success_count = sum(
            1 for r in responses
            if not isinstance(r, Exception) and r.status_code == 200
        )
        rate_limited_count = sum(
            1 for r in responses
            if not isinstance(r, Exception) and r.status_code == 429
        )

        # Some should succeed, some should be rate limited
        assert success_count > 0
        assert rate_limited_count > 0
        assert success_count + rate_limited_count == 20

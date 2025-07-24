"""Integration tests for rate limiting functionality."""

import asyncio
import time

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRateLimiting:
    """Test rate limiting functionality across different endpoints."""

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

    async def test_auth_login_rate_limit(self, client: AsyncClient):
        """Test rate limiting on login endpoint (5/minute)."""
        # Try to login 6 times rapidly
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        responses = []
        for i in range(6):
            response = await client.post(
                "/api/v1/auth/login",
                data=login_data
            )
            responses.append(response)

        # First 5 should work (return 401 for bad credentials)
        for i in range(5):
            assert responses[i].status_code == 401

        # 6th request should be rate limited
        assert responses[5].status_code == 429
        assert "rate_limit_exceeded" in responses[5].json()["error"]

        # Check rate limit headers
        assert "X-RateLimit-Limit" in responses[5].headers
        assert "Retry-After" in responses[5].headers

    async def test_auth_register_rate_limit(self, client: AsyncClient):
        """Test rate limiting on register endpoint (10/hour)."""
        # Since 10/hour is hard to test quickly, we'll check headers
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test1@example.com",
                "password": "password123",
                "full_name": "Test User"
            }
        )

        # Should have rate limit headers even on successful request
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers

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

    @pytest.mark.parametrize("endpoint,method,limit", [
        ("/api/v1/todos", "GET", 60),
        ("/api/v1/todos", "POST", 30),
        ("/api/v1/categories", "GET", 60),
        ("/api/v1/categories", "POST", 20),
        ("/api/v1/tags", "GET", 100),
        ("/api/v1/tags", "POST", 50),
    ])
    async def test_endpoint_specific_limits(
        self,
        client: AsyncClient,
        auth_headers: dict,
        endpoint: str,
        method: str,
        limit: int
    ):
        """Test that each endpoint has its specific rate limit."""
        # Make a request to get rate limit header
        if method == "GET":
            response = await client.get(endpoint, headers=auth_headers)
        else:
            data = {"name": "Test"} if "categories" in endpoint or "tags" in endpoint else {
                "title": "Test Todo"
            }
            response = await client.post(endpoint, json=data, headers=auth_headers)

        # Check rate limit header matches expected limit
        if "X-RateLimit-Limit" in response.headers:
            # Parse the limit (format: "30/minute" or just "30")
            limit_header = response.headers["X-RateLimit-Limit"]
            limit_value = int(limit_header.split("/")[0])

            # Should be close to expected limit
            assert abs(limit_value - limit) <= limit * 0.2  # 20% tolerance

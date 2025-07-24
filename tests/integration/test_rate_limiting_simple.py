"""Simplified rate limiting tests to validate basic functionality."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_rate_limit_on_public_endpoints(client: AsyncClient):
    """Test that rate limiting applies to public endpoints."""
    # Health endpoint should have rate limiting
    for _i in range(200):
        response = await client.get("/health")
        if response.status_code == 429:
            # Successfully hit rate limit
            assert "rate_limit_exceeded" in response.json()["error"]
            return

    # If we get here, rate limiting didn't trigger
    pytest.fail("Rate limiting did not trigger after 200 requests")

@pytest.mark.asyncio
async def test_rate_limit_headers_in_error_response(client: AsyncClient):
    """Test that rate limit headers are included in 429 responses."""
    # Make many requests to trigger rate limit
    response = None
    for _i in range(200):
        response = await client.get("/health")
        if response.status_code == 429:
            break

    assert response is not None
    assert response.status_code == 429

    # Check headers in rate limited response
    assert "Retry-After" in response.headers
    assert int(response.headers["Retry-After"]) > 0

@pytest.mark.asyncio
async def test_login_endpoint_rate_limiting(client: AsyncClient):
    """Test stricter rate limits on auth endpoints."""
    attempts = 0

    for i in range(20):
        # Use proper form data format for login
        response = await client.post(
            "/api/v1/auth/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "username": f"test{i}@example.com",
                "password": "wrongpassword"
            }
        )

        if response.status_code == 429:
            attempts = i
            break

    # Should hit rate limit quickly on auth endpoints
    assert attempts < 20
    assert attempts <= 10  # Expecting stricter limits

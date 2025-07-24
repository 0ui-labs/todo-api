"""Integration tests for monitoring and metrics."""
import pytest
from httpx import AsyncClient

from app.monitoring.metrics import (
    http_requests_total,
    todos_created_total,
    users_login_total,
    users_registered_total,
)


@pytest.mark.asyncio
async def test_metrics_endpoint_accessible(client: AsyncClient):
    """Test that the metrics endpoint is accessible."""
    response = await client.get("/metrics", follow_redirects=True)
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text
    assert "todos_created_total" in response.text


@pytest.mark.asyncio
async def test_http_request_metrics(client: AsyncClient):
    """Test that HTTP request metrics are tracked."""
    # Get initial metric value
    initial_value = 0
    for sample in http_requests_total.collect()[0].samples:
        if (sample.labels.get('method') == 'GET' and
            sample.labels.get('endpoint') == '/health' and
            sample.labels.get('status') == '200'):
            initial_value = sample.value
            break

    # Make a request
    response = await client.get("/health")
    assert response.status_code == 200

    # Check metric increased
    new_value = 0
    for sample in http_requests_total.collect()[0].samples:
        if (sample.labels.get('method') == 'GET' and
            sample.labels.get('endpoint') == '/health' and
            sample.labels.get('status') == '200'):
            new_value = sample.value
            break

    assert new_value > initial_value


@pytest.mark.asyncio
async def test_todo_creation_metrics(
    client: AsyncClient,
    auth_headers: dict
):
    """Test that todo creation metrics are tracked."""
    # Get initial metric value
    initial_value = todos_created_total._value.get()

    # Create a todo
    response = await client.post(
        "/api/v1/todos",
        json={
            "title": "Test Metric Todo",
            "description": "Testing metrics"
        },
        headers=auth_headers,
        follow_redirects=True
    )
    assert response.status_code == 201

    # Check metric increased
    new_value = todos_created_total._value.get()
    assert new_value > initial_value


@pytest.mark.asyncio
async def test_user_registration_metrics(client: AsyncClient):
    """Test that user registration metrics are tracked."""
    # Get initial metric value
    initial_value = users_registered_total._value.get()

    # Register a user
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "metrics_test@example.com",
            "password": "TestPassword123!",
            "name": "Metrics Test User"
        }
    )
    assert response.status_code == 201

    # Check metric increased
    new_value = users_registered_total._value.get()
    assert new_value > initial_value


@pytest.mark.asyncio
async def test_user_login_metrics(client: AsyncClient):
    """Test that user login metrics are tracked."""
    # First register a user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_metrics@example.com",
            "password": "TestPassword123!",
            "name": "Login Metrics User"
        }
    )

    # Get initial success metric value
    initial_success = 0
    for sample in users_login_total.collect()[0].samples:
        if sample.labels.get('status') == 'success':
            initial_success = sample.value
            break

    # Successful login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_metrics@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200

    # Check success metric increased
    new_success = 0
    for sample in users_login_total.collect()[0].samples:
        if sample.labels.get('status') == 'success':
            new_success = sample.value
            break

    assert new_success > initial_success

    # Get initial failure metric value
    initial_failure = 0
    for sample in users_login_total.collect()[0].samples:
        if sample.labels.get('status') == 'failure':
            initial_failure = sample.value
            break

    # Failed login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login_metrics@example.com",
            "password": "WrongPassword!"
        }
    )
    assert response.status_code == 401

    # Check failure metric increased
    new_failure = 0
    for sample in users_login_total.collect()[0].samples:
        if sample.labels.get('status') == 'failure':
            new_failure = sample.value
            break

    assert new_failure > initial_failure

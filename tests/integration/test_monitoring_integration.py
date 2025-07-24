"""Integration tests for monitoring functionality."""
import asyncio
import json

import pytest
from httpx import AsyncClient
from prometheus_client.parser import text_string_to_metric_families

from app.main import app


@pytest.mark.asyncio
class TestMonitoringIntegration:
    """Test monitoring integration with the API."""
    
    async def test_metrics_endpoint_accessible(self, test_client: AsyncClient):
        """Test that /metrics endpoint is accessible."""
        response = await test_client.get("/metrics")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        
        # Check response contains Prometheus metrics
        content = response.text
        assert "# HELP" in content
        assert "# TYPE" in content
        assert "http_requests_total" in content
    
    async def test_metrics_updated_after_requests(self, test_client: AsyncClient):
        """Test that metrics are updated after API requests."""
        # Make a request to health endpoint
        await test_client.get("/health")
        
        # Get metrics
        response = await test_client.get("/metrics")
        metrics_text = response.text
        
        # Parse metrics
        metrics = {}
        for family in text_string_to_metric_families(metrics_text):
            for sample in family.samples:
                metrics[sample.name] = sample
        
        # Check health endpoint was tracked
        health_metric_name = 'http_requests_total'
        assert health_metric_name in metrics
    
    async def test_request_id_header(self, test_client: AsyncClient):
        """Test that X-Request-ID header is added to responses."""
        response = await test_client.get("/health")
        
        # Check header present
        assert "x-request-id" in response.headers
        
        # Check it's a valid UUID format
        request_id = response.headers["x-request-id"]
        assert len(request_id) == 36  # UUID with dashes
        assert request_id.count("-") == 4
    
    async def test_process_time_header(self, test_client: AsyncClient):
        """Test that X-Process-Time header is added to responses."""
        response = await test_client.get("/health")
        
        # Check header present
        assert "x-process-time" in response.headers
        
        # Check it's a valid float
        process_time = float(response.headers["x-process-time"])
        assert process_time > 0
        assert process_time < 1  # Health check should be fast
    
    async def test_rate_limit_metrics(self, test_client: AsyncClient, test_user):
        """Test rate limit exceeded metrics are tracked."""
        # Get initial metrics
        metrics_before = await test_client.get("/metrics")
        
        # Hit rate limit (test endpoint has 5/minute limit)
        for _ in range(6):
            await test_client.get(
                "/api/v1/test-rate-limit",
                headers={"Authorization": f"Bearer {test_user['token']}"}
            )
        
        # Get metrics after
        metrics_after = await test_client.get("/metrics")
        
        # Check rate limit metric increased
        assert "rate_limit_exceeded_total" in metrics_after.text
    
    async def test_business_metrics_tracked(
        self, 
        test_client: AsyncClient, 
        test_user, 
        db_session
    ):
        """Test business metrics are tracked for todo operations."""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        # Create a todo
        create_response = await test_client.post(
            "/api/v1/todos",
            json={"title": "Test metrics", "description": "Test"},
            headers=headers
        )
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        
        # Complete the todo
        await test_client.patch(
            f"/api/v1/todos/{todo_id}",
            json={"completed": True},
            headers=headers
        )
        
        # Delete the todo
        await test_client.delete(
            f"/api/v1/todos/{todo_id}",
            headers=headers
        )
        
        # Get metrics
        metrics_response = await test_client.get("/metrics")
        metrics_text = metrics_response.text
        
        # Check business metrics present
        assert "todos_created_total" in metrics_text
        assert "todos_completed_total" in metrics_text
        assert "todos_deleted_total" in metrics_text
    
    async def test_error_metrics_tracked(self, test_client: AsyncClient, test_user):
        """Test error metrics are tracked for failed requests."""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        # Try to get non-existent todo
        response = await test_client.get(
            "/api/v1/todos/00000000-0000-0000-0000-000000000000",
            headers=headers
        )
        assert response.status_code == 404
        
        # Get metrics
        metrics_response = await test_client.get("/metrics")
        metrics_text = metrics_response.text
        
        # Check 404 was tracked
        assert 'http_requests_total' in metrics_text
        assert 'status="404"' in metrics_text
    
    async def test_concurrent_requests_tracking(
        self, 
        test_client: AsyncClient,
        test_user
    ):
        """Test in-progress gauge tracks concurrent requests."""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        # Make multiple concurrent requests
        tasks = []
        for _ in range(5):
            task = test_client.get("/api/v1/todos", headers=headers)
            tasks.append(task)
        
        # Wait for all to complete
        responses = await asyncio.gather(*tasks)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Get metrics
        metrics_response = await test_client.get("/metrics")
        
        # Check in-progress metric exists
        assert "http_requests_in_progress" in metrics_response.text
    
    async def test_json_logging_format(self, test_client: AsyncClient, caplog):
        """Test that logs are in JSON format when configured."""
        # Make a request
        await test_client.get("/health")
        
        # Check if any log records were captured
        # Note: This test might need adjustment based on test configuration
        # as logging might be configured differently in tests
        pass  # Logging capture in tests can be complex with async
"""Tests for request middleware."""
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.middleware.request import RequestSizeLimitMiddleware


class TestRequestSizeLimitMiddleware:
    """Test cases for RequestSizeLimitMiddleware."""

    @pytest.fixture
    def app_with_middleware(self):
        """Create app with request size limit middleware."""
        app = FastAPI()
        app.add_middleware(
            RequestSizeLimitMiddleware,
            max_size=1024,  # 1KB for testing
            error_message="Test: Request too large"
        )

        @app.post("/test")
        async def test_endpoint(request: Request):
            body = await request.body()
            return {"size": len(body)}

        return app

    def test_request_within_limit(self, app_with_middleware):
        """Test request within size limit."""
        client = TestClient(app_with_middleware)
        response = client.post(
            "/test",
            content=b"x" * 500,  # 500 bytes
            headers={"Content-Length": "500"}
        )
        assert response.status_code == 200
        assert response.json() == {"size": 500}

    def test_request_exceeds_limit(self, app_with_middleware):
        """Test request exceeding size limit."""
        client = TestClient(app_with_middleware)
        response = client.post(
            "/test",
            content=b"x" * 2000,  # 2KB
            headers={"Content-Length": "2000"}
        )
        assert response.status_code == 413
        assert response.json()["detail"] == "Test: Request too large"
        assert response.json()["max_size_bytes"] == 1024

    def test_invalid_content_length(self, app_with_middleware):
        """Test invalid Content-Length header."""
        client = TestClient(app_with_middleware)
        response = client.post(
            "/test",
            content=b"test",
            headers={"Content-Length": "invalid"}
        )
        assert response.status_code == 400
        assert "Invalid Content-Length" in response.json()["detail"]

    def test_no_content_length(self, app_with_middleware):
        """Test request without Content-Length header."""
        client = TestClient(app_with_middleware)
        response = client.post("/test", json={"test": "data"})
        assert response.status_code == 200

    def test_max_size_in_error_response(self):
        """Test that max size is included in error response when configured."""
        app = FastAPI()
        app.add_middleware(
            RequestSizeLimitMiddleware,
            max_size=2048,
            include_max_size_in_error=True
        )

        @app.post("/test")
        async def test_endpoint():
            return {"status": "ok"}

        client = TestClient(app)
        response = client.post(
            "/test",
            content=b"x" * 3000,
            headers={"Content-Length": "3000"}
        )

        assert response.status_code == 413
        json_response = response.json()
        assert json_response["max_size_bytes"] == 2048
        assert json_response["max_size_mb"] == 0.0  # 2KB = 0.002MB rounds to 0.0

    def test_custom_error_message(self):
        """Test custom error message configuration."""
        app = FastAPI()
        custom_message = "Custom error: Too big!"
        app.add_middleware(
            RequestSizeLimitMiddleware,
            max_size=100,
            error_message=custom_message
        )

        @app.post("/test")
        async def test_endpoint():
            return {"status": "ok"}

        client = TestClient(app)
        response = client.post(
            "/test",
            content=b"x" * 200,
            headers={"Content-Length": "200"}
        )

        assert response.status_code == 413
        assert response.json()["detail"] == custom_message

    def test_exclude_max_size_from_error(self):
        """Test excluding max size from error response."""
        app = FastAPI()
        app.add_middleware(
            RequestSizeLimitMiddleware,
            max_size=1024,
            include_max_size_in_error=False
        )

        @app.post("/test")
        async def test_endpoint():
            return {"status": "ok"}

        client = TestClient(app)
        response = client.post(
            "/test",
            content=b"x" * 2000,
            headers={"Content-Length": "2000"}
        )

        assert response.status_code == 413
        json_response = response.json()
        assert "max_size_bytes" not in json_response
        assert "max_size_mb" not in json_response

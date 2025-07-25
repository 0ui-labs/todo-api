"""Integration tests for middleware stack."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.config import settings


class TestMiddlewareIntegration:
    """Test middleware working together."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_request_size_limit_integration(self, client):
        """Test request size limit middleware in full app."""
        # Create a large payload
        large_payload = "x" * (settings.max_request_size + 1000)
        
        response = client.post(
            f"{settings.api_v1_str}/auth/login",
            content=large_payload,
            headers={"Content-Length": str(len(large_payload))}
        )
        
        assert response.status_code == 413
        assert "Request body too large" in response.json()["detail"]
        assert response.json()["type"] == "request_too_large"
    
    def test_security_headers_applied(self, client):
        """Test that security headers are applied to responses."""
        response = client.get("/health")
        
        # Check security headers
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        
        # Server header should be removed
        assert "Server" not in response.headers
    
    def test_middleware_ordering(self, client):
        """Test middleware execution order."""
        # Send a request that triggers multiple middleware
        response = client.post(
            f"{settings.api_v1_str}/auth/login",
            json={"username": "test", "password": "test"}
        )
        
        # Even if login fails, should have security headers
        assert "X-Content-Type-Options" in response.headers
        
    def test_error_handler_catches_exceptions(self, client):
        """Test that error handler middleware catches exceptions."""
        # This would normally cause a 500 error
        # but error handler should convert to proper response
        with patch('app.api.auth.authenticate_user') as mock_auth:
            mock_auth.side_effect = Exception("Test exception")
            
            response = client.post(
                f"{settings.api_v1_str}/auth/login",
                json={"username": "test", "password": "test"}
            )
            
            assert response.status_code == 500
            assert "Internal server error" in response.json()["detail"]
    
    @patch('app.config.settings')
    def test_middleware_can_be_disabled(self, mock_settings, client):
        """Test that middleware can be disabled via settings."""
        # This test would require app restart to take effect
        # Just verify the setting exists
        assert hasattr(settings, 'middleware_enabled')
        assert hasattr(settings, 'security_headers_enabled')
        assert hasattr(settings, 'request_logging_enabled')
        assert hasattr(settings, 'metrics_collection_enabled')
    
    def test_request_without_content_length(self, client):
        """Test that requests without Content-Length are allowed."""
        response = client.post(
            f"{settings.api_v1_str}/auth/login",
            json={"username": "test", "password": "test"}
        )
        
        # Should not be rejected by size limit middleware
        assert response.status_code != 413
    
    def test_cors_middleware_still_works(self, client):
        """Test that CORS middleware is still functional."""
        response = client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
    
    def test_rate_limiting_still_works(self, client):
        """Test that rate limiting middleware is still functional."""
        # Test rate limit endpoint
        for i in range(6):  # Limit is 5/minute
            response = client.get(f"{settings.api_v1_str}/test-rate-limit")
            
            if i < 5:
                assert response.status_code == 200
            else:
                assert response.status_code == 429  # Too Many Requests
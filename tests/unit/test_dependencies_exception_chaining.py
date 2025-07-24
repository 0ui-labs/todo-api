"""Test exception chaining for dependencies module."""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError

from app.dependencies import get_current_user_id


class TestDependenciesExceptionChaining:
    """Test that exceptions in dependencies properly chain with 'from' clause."""

    @pytest.mark.asyncio
    async def test_get_current_user_jwt_error_chaining(self) -> None:
        """Test that JWTError is correctly chained with HTTPException."""
        # Mock credentials with invalid token
        mock_credentials = MagicMock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "invalid.jwt.token"

        # Mock jwt.decode to raise JWTError
        with patch('app.dependencies.jwt.decode') as mock_decode:
            mock_decode.side_effect = JWTError("Invalid token format")

            try:
                await get_current_user_id(credentials=mock_credentials)
                pytest.fail("Expected HTTPException to be raised")
            except HTTPException as e:
                # Check that the exception was raised with proper chaining
                assert e.__cause__ is not None, "HTTPException should have a __cause__"
                assert isinstance(e.__cause__, JWTError), "Cause should be JWTError"
                assert str(e.__cause__) == "Invalid token format"
                assert e.status_code == 401
                assert e.detail == "Invalid authentication credentials"
                assert e.headers == {"WWW-Authenticate": "Bearer"}

    @pytest.mark.asyncio
    async def test_get_current_user_jwt_expired_chaining(self) -> None:
        """Test that expired token error is properly chained."""
        mock_credentials = MagicMock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "expired.jwt.token"

        # Mock jwt.decode to raise JWTError for expired token
        with patch('app.dependencies.jwt.decode') as mock_decode:
            mock_decode.side_effect = JWTError("Token has expired")

            try:
                await get_current_user_id(credentials=mock_credentials)
                pytest.fail("Expected HTTPException to be raised")
            except HTTPException as e:
                # Verify exception chaining
                assert e.__cause__ is not None
                assert isinstance(e.__cause__, JWTError)
                assert "expired" in str(e.__cause__).lower()

    @pytest.mark.asyncio
    async def test_get_current_user_jwt_invalid_signature_chaining(self) -> None:
        """Test that invalid signature error is properly chained."""
        mock_credentials = MagicMock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "token.with.invalid.signature"

        # Mock jwt.decode to raise JWTError for invalid signature
        with patch('app.dependencies.jwt.decode') as mock_decode:
            mock_decode.side_effect = JWTError("Signature verification failed")

            try:
                await get_current_user_id(credentials=mock_credentials)
                pytest.fail("Expected HTTPException to be raised")
            except HTTPException as e:
                # Verify exception chaining
                assert e.__cause__ is not None
                assert isinstance(e.__cause__, JWTError)
                assert "signature" in str(e.__cause__).lower()

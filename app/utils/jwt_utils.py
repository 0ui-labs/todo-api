"""JWT utility functions with async support."""

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from app.config import settings


async def create_access_token_async(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
    token_version: int = 0
) -> str:
    """Create a JWT access token with JTI for revocation support (async version).

    Args:
        data: Token payload data
        expires_delta: Optional token expiration time
        token_version: User's current token version (for revocation)

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    # Add JWT ID (jti) for token revocation
    jti = str(uuid.uuid4())

    to_encode.update({
        "exp": expire,
        "jti": jti,
        "token_version": token_version
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return str(encoded_jwt)

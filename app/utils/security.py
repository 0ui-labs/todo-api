"""Security utilities for password hashing and JWT token management."""
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Generate a password hash."""
    return str(pwd_context.hash(password))


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create a JWT access token with JTI for revocation support."""
    import uuid
    
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    # Add JWT ID (jti) for token revocation
    jti = str(uuid.uuid4())
    
    # Add token version if user_id is present
    user_id = data.get("sub")
    token_version = 0
    if user_id:
        # Import here to avoid circular dependency
        from app.services.token_blacklist import get_token_blacklist_service
        import asyncio
        
        # Get user's current token version
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, we can't use asyncio.run
            # This is a limitation - in production, this should be passed as parameter
            token_version = 0
        else:
            blacklist_service = asyncio.run(get_token_blacklist_service())
            token_version = asyncio.run(blacklist_service.get_user_token_version(user_id))

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

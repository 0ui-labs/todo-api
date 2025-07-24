"""Common dependencies for the application."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db

# Security scheme
security = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    """Extract and validate user ID from JWT token, checking blacklist."""
    from app.services.token_blacklist import get_token_blacklist_service

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token is blacklisted by JTI
        jti = payload.get("jti")
        if jti:
            blacklist_service = await get_token_blacklist_service()
            if await blacklist_service.is_token_blacklisted(jti):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Check token version if present
        token_version = payload.get("token_version", 0)
        if token_version is not None:
            blacklist_service = await get_token_blacklist_service()
            current_version = await blacklist_service.get_user_token_version(user_id)
            if token_version < current_version:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return user_id
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


# Dependency annotations for cleaner code
CurrentUser = Annotated[str, Depends(get_current_user_id)]
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]

"""Authentication endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from redis.exceptions import RedisError

from app.config import settings
from app.dependencies import CurrentUser, DatabaseSession
from app.middleware.rate_limit import RateLimiters
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService
from app.services.exceptions import AccountLockedError, InvalidCredentialsError

logger = logging.getLogger(__name__)

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account",
)
@RateLimiters.auth_register
async def register(
    request: Request,
    user_data: UserCreate,
    db: DatabaseSession,
) -> UserResponse:
    """Register a new user."""
    service = AuthService(db)

    try:
        user = await service.register_user(user_data)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate user and receive access token",
)
@RateLimiters.auth_login
async def login(
    request: Request,
    login_data: UserLogin,
    db: DatabaseSession,
) -> TokenResponse:
    """Login user and return access token."""
    auth_service = AuthService(db)

    try:
        # Perform login with rate limiting
        user = await auth_service.login_user(login_data)

        # Create access token
        access_token, expires_in = await auth_service.create_user_token(user.id)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        )

    except AccountLockedError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": str(e),
                "locked_until": e.locked_until.isoformat(),
                "remaining_seconds": e.remaining_seconds,
                "failed_attempts": e.failed_attempts
            },
            headers={"Retry-After": str(e.remaining_seconds)},
        ) from e
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": str(e),
                "remaining_attempts": e.remaining_attempts,
                "failed_attempts": e.failed_attempts
            },
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user_id: CurrentUser,
    token_creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> None:
    """Logout the current user by revoking their token.

    This adds the current token to the blacklist, preventing its further use.
    """
    from jose import jwt

    from app.services.token_blacklist import get_token_blacklist_service

    token = token_creds.credentials

    try:
        # Decode token to get JTI and expiration
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )

        jti = payload.get("jti")
        exp = payload.get("exp")

        if jti:
            # Add token to blacklist
            blacklist_service = await get_token_blacklist_service()
            exp_datetime = None
            if exp:
                from datetime import UTC, datetime
                exp_datetime = datetime.fromtimestamp(exp, tz=UTC)

            await blacklist_service.add_token_to_blacklist(
                jti=jti,
                user_id=current_user_id,
                exp=exp_datetime
            )
    except JWTError as e:
        # Ein ungültiges Token ist kein Serverfehler, sollte aber geloggt werden.
        logger.warning(
            f"JWTError during logout, token might be invalid: {e}", exc_info=True
        )
        # Trotzdem erfolgreich für den Client, da er sich abmelden wollte.
        pass
    except RedisError as e:
        # Ein Redis-Fehler ist ein kritisches Infrastrukturproblem.
        logger.error(
            f"RedisError during logout, token could not be blacklisted: {e}",
            exc_info=True
        )
        # Trotzdem erfolgreich für den Client.
        pass
    except Exception as e:
        # Fängt alle anderen unerwarteten Fehler ab.
        logger.exception(f"An unexpected error occurred during logout: {e}")
        # Trotzdem erfolgreich für den Client.
        pass


@router.post("/logout-all-devices", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all_devices(
    current_user_id: CurrentUser,
) -> None:
    """Logout from all devices by revoking all user tokens.

    This increments the user's token version, invalidating all existing tokens.
    """
    from app.services.token_blacklist import get_token_blacklist_service

    blacklist_service = await get_token_blacklist_service()
    await blacklist_service.revoke_all_user_tokens(current_user_id)

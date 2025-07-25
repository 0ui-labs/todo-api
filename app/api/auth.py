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
    from app.services.login_rate_limit import LoginRateLimitService

    # Initialize services
    auth_service = AuthService(db)
    rate_limit_service = LoginRateLimitService()

    try:
        # Check if user is rate limited
        is_allowed, locked_until, attempts = await rate_limit_service.check_rate_limit(
            login_data.email
        )

        if not is_allowed and locked_until:
            # Calculate remaining lockout time
            from datetime import datetime
            remaining_seconds = int((locked_until - datetime.utcnow()).total_seconds())

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": "Too many failed login attempts. Account is locked.",
                    "locked_until": locked_until.isoformat(),
                    "remaining_seconds": remaining_seconds,
                    "failed_attempts": attempts
                },
                headers={"Retry-After": str(remaining_seconds)},
            )

        # Authenticate user
        user = await auth_service.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        if not user:
            # Record failed attempt
            attempts, lockout_until = await rate_limit_service.record_failed_attempt(
                login_data.email
            )
            current_attempts = attempts

            if lockout_until:
                # Account just got locked
                remaining_seconds = int(
                    (lockout_until - datetime.utcnow()).total_seconds()
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "message": (
                            "Too many failed login attempts. Account is now locked."
                        ),
                        "locked_until": lockout_until.isoformat(),
                        "remaining_seconds": remaining_seconds,
                        "failed_attempts": current_attempts
                    },
                    headers={"Retry-After": str(remaining_seconds)},
                )
            else:
                # Regular failed login
                remaining_attempts = max(
                    0, rate_limit_service.max_attempts - current_attempts
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "message": "Invalid email or password",
                        "remaining_attempts": remaining_attempts,
                        "failed_attempts": current_attempts
                    },
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Clear failed attempts on successful login
        await rate_limit_service.clear_failed_attempts(login_data.email)

        # Create access token
        access_token, expires_in = await auth_service.create_user_token(user.id)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        )

    finally:
        # Clean up
        await rate_limit_service.close()

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

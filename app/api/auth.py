"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, Request, status

from app.config import settings
from app.dependencies import CurrentUser, DatabaseSession
from app.middleware.rate_limit import RateLimiters
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter()


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
    service = AuthService(db)

    # Authenticate user
    user = await service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token, expires_in = await service.create_user_token(user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    current_user_id: CurrentUser,
) -> None:
    """Logout the current user by revoking their token.

    This adds the current token to the blacklist, preventing its further use.
    """
    from jose import jwt

    from app.services.token_blacklist import get_token_blacklist_service

    # Extract token from request
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

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
    except Exception as e:
        # Log error but don't fail the logout
        print(f"Error during logout: {e}")
        # Even if blacklisting fails, we return success to the user
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

"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, Request, status

from app.dependencies import DatabaseSession
from app.middleware.rate_limit import limiter
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
@limiter.limit("10/hour")  # Nur 10 Registrierungen pro Stunde
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
@limiter.limit("5/minute")  # Nur 5 Login-Versuche pro Minute
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
    access_token, expires_in = service.create_user_token(user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=expires_in,
    )

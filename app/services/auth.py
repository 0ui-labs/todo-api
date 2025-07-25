"""Authentication service layer."""
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.monitoring.metrics import users_login_total, users_registered_total
from app.schemas.user import UserCreate, UserLogin
from app.services.exceptions import AccountLockedError, InvalidCredentialsError
from app.services.login_rate_limit import LoginRateLimitService
from app.utils.jwt_utils import create_access_token_async as create_access_token
from app.utils.security import (
    get_password_hash,
    verify_password,
)


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: AsyncSession):
        """Initialize the service with database session."""
        self.db = db

    async def register_user(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if user already exists
        query = select(User).where(User.email == user_data.email)
        result = await self.db.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("User with this email already exists")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=hashed_password,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # Track metric
        users_registered_total.inc()

        return user

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> User | None:
        """Authenticate a user by email and password."""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            users_login_total.labels(status="failure").inc()
            return None

        if not verify_password(password, user.password_hash):
            users_login_total.labels(status="failure").inc()
            return None

        if not user.is_active:
            users_login_total.labels(status="failure").inc()
            return None

        users_login_total.labels(status="success").inc()
        return user

    async def login_user(self, login_data: UserLogin) -> User:
        """Handle user login with rate limiting and authentication."""
        rate_limit_service = LoginRateLimitService()

        try:
            # Check if user is rate limited
            check_result = await rate_limit_service.check_rate_limit(
                login_data.email
            )
            is_allowed, locked_until, attempts = check_result

            if not is_allowed and locked_until:
                # Calculate remaining lockout time
                remaining_seconds = int(
                    (locked_until - datetime.utcnow()).total_seconds()
                )

                raise AccountLockedError(
                    message="Too many failed login attempts. Account is locked.",
                    locked_until=locked_until,
                    remaining_seconds=remaining_seconds,
                    failed_attempts=attempts
                )

            # Authenticate user
            user = await self.authenticate_user(
                email=login_data.email,
                password=login_data.password
            )

            if not user:
                # Record failed attempt
                record_result = await rate_limit_service.record_failed_attempt(
                    login_data.email
                )
                attempts, lockout_until = record_result
                current_attempts = attempts

                if lockout_until:
                    # Account just got locked
                    remaining_seconds = int(
                        (lockout_until - datetime.utcnow()).total_seconds()
                    )
                    raise AccountLockedError(
                        message=(
                            "Too many failed login attempts. Account is now locked."
                        ),
                        locked_until=lockout_until,
                        remaining_seconds=remaining_seconds,
                        failed_attempts=current_attempts
                    )
                else:
                    # Regular failed login
                    remaining_attempts = max(
                        0, rate_limit_service.max_attempts - current_attempts
                    )
                    raise InvalidCredentialsError(
                        message="Invalid email or password",
                        remaining_attempts=remaining_attempts,
                        failed_attempts=current_attempts
                    )

            # Clear failed attempts on successful login
            await rate_limit_service.clear_failed_attempts(login_data.email)

            return user

        finally:
            # Clean up
            await rate_limit_service.close()

    async def create_user_token(self, user_id: UUID) -> tuple[str, int]:
        """Create an access token for a user."""
        from app.services.token_blacklist import get_token_blacklist_service

        # Get user's current token version
        blacklist_service = await get_token_blacklist_service()
        token_version = await blacklist_service.get_user_token_version(str(user_id))

        access_token = await create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            token_version=token_version
        )
        return access_token, settings.access_token_expire_minutes * 60

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get a user by ID."""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

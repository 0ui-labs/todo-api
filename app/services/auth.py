"""Authentication service layer."""
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.monitoring.metrics import users_registered_total, users_login_total


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

    async def create_user_token(self, user_id: UUID) -> tuple[str, int]:
        """Create an access token for a user."""
        from app.services.token_blacklist import get_token_blacklist_service
        from app.utils.jwt_utils import create_access_token_async
        
        # Get user's current token version
        blacklist_service = await get_token_blacklist_service()
        token_version = await blacklist_service.get_user_token_version(str(user_id))
        
        access_token = await create_access_token_async(
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

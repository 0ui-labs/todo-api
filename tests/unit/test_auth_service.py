"""Unit tests for authentication service."""
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import AuthService
from app.utils.security import get_password_hash, verify_password

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = AsyncMock(spec=AsyncSession)
    mock.commit = AsyncMock()
    mock.refresh = AsyncMock()
    mock.add = MagicMock()
    return mock


@pytest.fixture
def auth_service(mock_db):
    """Create an AuthService instance with mock db."""
    return AuthService(mock_db)


@pytest.fixture
def sample_user():
    """Create a sample user."""
    return User(
        id=uuid4(),
        email="test@example.com",
        password_hash=get_password_hash("TestPassword123!"),
        name="Test User",
        is_active=True,
    )


@pytest.fixture
def sample_user_create():
    """Create a sample UserCreate schema."""
    return UserCreate(
        email="newuser@example.com",
        password="StrongPass123!",
        name="New User"
    )


class TestAuthService:
    """Test cases for AuthService."""

    async def test_register_user_success(
        self, auth_service, mock_db, sample_user_create
    ):
        """Test successful user registration."""
        # Mock query result - no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.register_user(sample_user_create)

        # Verify the result
        assert result is not None
        assert result.email == sample_user_create.email
        assert result.name == sample_user_create.name

        # Verify user was created
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called

        # Verify the user object was created correctly
        user_arg = mock_db.add.call_args[0][0]
        assert isinstance(user_arg, User)
        assert user_arg.email == sample_user_create.email
        assert user_arg.name == sample_user_create.name
        assert verify_password(
            sample_user_create.password, user_arg.password_hash
        )

    async def test_register_user_duplicate_email(
        self, auth_service, mock_db, sample_user, sample_user_create
    ):
        """Test registration with duplicate email."""
        # Mock query result - existing user found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db.execute.return_value = mock_result

        # Should raise ValueError
        with pytest.raises(ValueError, match="User with this email already exists"):
            await auth_service.register_user(sample_user_create)

        # Verify no user was added
        assert not mock_db.add.called
        assert not mock_db.commit.called

    async def test_authenticate_user_success(
        self, auth_service, mock_db, sample_user
    ):
        """Test successful user authentication."""
        # Mock query result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.authenticate_user(
            sample_user.email, "TestPassword123!"
        )

        # Verify result
        assert result == sample_user

    async def test_authenticate_user_wrong_password(
        self, auth_service, mock_db, sample_user
    ):
        """Test authentication with wrong password."""
        # Mock query result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db.execute.return_value = mock_result

        # Call the method with wrong password
        result = await auth_service.authenticate_user(
            sample_user.email, "wrongpassword"
        )

        # Verify result
        assert result is None

    async def test_authenticate_user_not_found(self, auth_service, mock_db):
        """Test authentication with non-existent user."""
        # Mock query result - no user found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.authenticate_user(
            "nonexistent@example.com", "password"
        )

        # Verify result
        assert result is None

    async def test_authenticate_user_inactive(
        self, auth_service, mock_db, sample_user
    ):
        """Test authentication with inactive user."""
        # Make user inactive
        sample_user.is_active = False

        # Mock query result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.authenticate_user(
            sample_user.email, "TestPassword123!"
        )

        # Verify result
        assert result is None

    async def test_create_user_token(self, auth_service, sample_user):
        """Test user token creation."""
        # Mock token blacklist service
        mock_blacklist = AsyncMock()
        mock_blacklist.get_user_token_version.return_value = 1

        with patch('app.services.token_blacklist.get_token_blacklist_service', return_value=mock_blacklist):
            # Call the method
            token, expires_in = await auth_service.create_user_token(sample_user.id)

            # Verify token contains correct version
            payload = jwt.decode(
                token,
                settings.secret_key.get_secret_value(),
                algorithms=[settings.algorithm]
            )
            assert payload["sub"] == str(sample_user.id)
            assert payload["token_version"] == 1
            assert "exp" in payload
            assert expires_in == settings.access_token_expire_minutes * 60

    async def test_get_user_by_id_success(self, auth_service, mock_db, sample_user):
        """Test getting user by ID."""
        # Mock query result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.get_user_by_id(sample_user.id)

        # Verify result
        assert result == sample_user

    async def test_get_user_by_id_not_found(self, auth_service, mock_db):
        """Test getting non-existent user by ID."""
        # Mock query result - no user found
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        # Call the method
        result = await auth_service.get_user_by_id(uuid4())

        # Verify result
        assert result is None

    async def test_register_user_database_error(
        self, auth_service, mock_db, sample_user_create
    ):
        """Test user registration with database error."""
        # Mock query result - no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        # Mock database error on commit
        mock_db.commit.side_effect = IntegrityError("", "", "")

        # Should raise IntegrityError
        with pytest.raises(IntegrityError):
            await auth_service.register_user(sample_user_create)

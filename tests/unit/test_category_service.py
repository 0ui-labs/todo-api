"""Unit tests for CategoryService."""
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category import CategoryService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = AsyncMock(spec=AsyncSession)
    return mock


@pytest.fixture
def category_service(mock_db):
    """Create a CategoryService instance with mock db."""
    return CategoryService(mock_db)


@pytest.fixture
def sample_category():
    """Create a sample category."""
    return Category(
        id=uuid4(),
        user_id=uuid4(),
        name="Work",
        color="#FF5733",
    )


@pytest.fixture
def sample_category_create():
    """Create a sample CategoryCreate schema."""
    return CategoryCreate(name="Work", color="#FF5733")


@pytest.fixture
def sample_category_update():
    """Create a sample CategoryUpdate schema."""
    return CategoryUpdate(name="Personal", color="#00FF00")


class TestCategoryService:
    """Test CategoryService methods."""

    async def test_create_category_success(
        self, category_service, mock_db, sample_category_create
    ) -> None:
        """Test successful category creation."""
        user_id = uuid4()

        # Mock the database operations
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Call the method
        result = await category_service.create_category(user_id, sample_category_create)

        # Assertions
        assert result.user_id == user_id
        assert result.name == sample_category_create.name
        assert result.color == sample_category_create.color
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    async def test_create_category_duplicate_name(
        self, category_service, mock_db, sample_category_create
    ) -> None:
        """Test category creation with duplicate name."""
        user_id = uuid4()

        # Mock IntegrityError for duplicate name
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock(side_effect=IntegrityError(
            "duplicate key",
            "INSERT INTO categories",
            "uq_user_category_name"
        ))
        mock_db.rollback = AsyncMock()

        # Create mock IntegrityError with orig attribute
        error = IntegrityError(
            "duplicate key",
            "INSERT INTO categories",
            "uq_user_category_name"
        )
        error.orig = MagicMock()
        error.orig.__str__ = MagicMock(return_value="uq_user_category_name")
        mock_db.commit.side_effect = error

        # Call the method and expect ValueError
        with pytest.raises(
            ValueError, match="A category with this name already exists"
        ):
            await category_service.create_category(
                user_id, sample_category_create
            )

        mock_db.rollback.assert_called_once()

    async def test_get_category_found(
        self, category_service, mock_db, sample_category
    ) -> None:
        """Test getting an existing category."""
        category_id = sample_category.id
        user_id = sample_category.user_id

        # Mock the database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_category
        mock_db.execute = AsyncMock(return_value=mock_result)

        # Call the method
        result = await category_service.get_category(category_id, user_id)

        # Assertions
        assert result == sample_category
        mock_db.execute.assert_called_once()

    async def test_get_category_not_found(
        self, category_service, mock_db
    ) -> None:
        """Test getting a non-existent category."""
        category_id = uuid4()
        user_id = uuid4()

        # Mock the database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        # Call the method
        result = await category_service.get_category(category_id, user_id)

        # Assertions
        assert result is None
        mock_db.execute.assert_called_once()

    async def test_get_categories_with_search(
        self, category_service, mock_db, sample_category
    ) -> None:
        """Test getting categories with search filter."""
        user_id = sample_category.user_id

        # Mock the database queries
        mock_count_result = MagicMock()
        mock_count_result.scalar_one.return_value = 1

        mock_categories_result = MagicMock()
        mock_categories_result.scalars.return_value.all.return_value = [sample_category]

        mock_db.execute = AsyncMock(
            side_effect=[mock_count_result, mock_categories_result]
        )

        # Call the method
        categories, total = await category_service.get_categories(
            user_id=user_id,
            limit=20,
            offset=0,
            search="Work",
            sort_by="created_at",
            order="desc"
        )

        # Assertions
        assert len(categories) == 1
        assert total == 1
        assert categories[0] == sample_category
        assert mock_db.execute.call_count == 2

    async def test_update_category_success(
        self, category_service, mock_db, sample_category, sample_category_update
    ) -> None:
        """Test successful category update."""
        category_id = sample_category.id
        user_id = sample_category.user_id

        # Mock get_category to return the existing category
        with patch.object(
            category_service, 'get_category', return_value=sample_category
        ):
            mock_db.commit = AsyncMock()
            mock_db.refresh = AsyncMock()

            # Call the method
            result = await category_service.update_category(
                category_id, user_id, sample_category_update
            )

            # Assertions
            assert result.name == sample_category_update.name
            assert result.color == sample_category_update.color
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()

    async def test_update_category_not_found(
        self, category_service, mock_db, sample_category_update
    ) -> None:
        """Test updating a non-existent category."""
        category_id = uuid4()
        user_id = uuid4()

        # Mock get_category to return None
        with patch.object(category_service, 'get_category', return_value=None):
            # Call the method
            result = await category_service.update_category(
                category_id, user_id, sample_category_update
            )

            # Assertions
            assert result is None

    async def test_update_category_duplicate_name(
        self, category_service, mock_db, sample_category, sample_category_update
    ) -> None:
        """Test category update with duplicate name."""
        category_id = sample_category.id
        user_id = sample_category.user_id

        # Mock get_category to return the existing category
        with patch.object(
            category_service, 'get_category', return_value=sample_category
        ):
            # Mock IntegrityError for duplicate name
            error = IntegrityError(
                "duplicate key",
                "UPDATE categories",
                "uq_user_category_name"
            )
            error.orig = MagicMock()
            error.orig.__str__ = MagicMock(return_value="uq_user_category_name")
            mock_db.commit = AsyncMock(side_effect=error)
            mock_db.rollback = AsyncMock()

            # Call the method and expect ValueError
            with pytest.raises(
                ValueError, match="A category with this name already exists"
            ):
                await category_service.update_category(
                    category_id, user_id, sample_category_update
                )

            mock_db.rollback.assert_called_once()

    async def test_delete_category_success(
        self, category_service, mock_db, sample_category
    ) -> None:
        """Test successful category deletion."""
        category_id = sample_category.id
        user_id = sample_category.user_id

        # Mock get_category to return the existing category
        with patch.object(
            category_service, 'get_category', return_value=sample_category
        ):
            mock_db.delete = AsyncMock()
            mock_db.commit = AsyncMock()

            # Call the method
            result = await category_service.delete_category(category_id, user_id)

            # Assertions
            assert result is True
            mock_db.delete.assert_called_once_with(sample_category)
            mock_db.commit.assert_called_once()

    async def test_delete_category_not_found(
        self, category_service, mock_db
    ) -> None:
        """Test deleting a non-existent category."""
        category_id = uuid4()
        user_id = uuid4()

        # Mock get_category to return None
        with patch.object(category_service, 'get_category', return_value=None):
            # Call the method
            result = await category_service.delete_category(category_id, user_id)

            # Assertions
            assert result is False

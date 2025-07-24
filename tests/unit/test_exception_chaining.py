"""Test exception chaining for proper error handling."""
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.categories import create_category, update_category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category import CategoryService


class TestExceptionChaining:
    """Test that exceptions properly chain with 'from' clause."""

    @pytest.mark.asyncio
    async def test_create_category_exception_chaining_api(self) -> None:
        """Test that API layer properly chains exceptions."""
        # Mock dependencies
        mock_user = str(uuid4())
        mock_db = AsyncMock()
        category_data = CategoryCreate(name="Test", color="#FF0000")

        # Create a mock service that raises ValueError
        mock_service = AsyncMock()
        mock_service.create_category.side_effect = ValueError(
            "A category with this name already exists"
        )

        with patch('app.api.categories.CategoryService', return_value=mock_service):
            try:
                await create_category(category_data, mock_user, mock_db)
            except HTTPException as e:
                # Check that the exception was raised with proper chaining
                assert e.__cause__ is not None
                assert isinstance(e.__cause__, ValueError)
                assert str(e.__cause__) == "A category with this name already exists"

    @pytest.mark.asyncio
    async def test_update_category_exception_chaining_api(self) -> None:
        """Test that update API endpoint properly chains exceptions."""
        # Mock dependencies
        mock_user = str(uuid4())
        mock_db = AsyncMock()
        category_id = uuid4()
        category_update = CategoryUpdate(name="Updated")

        # Create a mock service that raises ValueError
        mock_service = AsyncMock()
        mock_service.update_category.side_effect = ValueError(
            "A category with this name already exists"
        )

        with patch('app.api.categories.CategoryService', return_value=mock_service):
            try:
                await update_category(category_id, category_update, mock_user, mock_db)
            except HTTPException as e:
                # Check that the exception was raised with proper chaining
                assert e.__cause__ is not None
                assert isinstance(e.__cause__, ValueError)
                assert str(e.__cause__) == "A category with this name already exists"

    @pytest.mark.asyncio
    async def test_create_category_exception_chaining_service(self) -> None:
        """Test that service layer properly chains IntegrityError."""
        mock_db = AsyncMock()
        service = CategoryService(mock_db)
        user_id = uuid4()
        category_data = CategoryCreate(name="Test", color="#FF0000")

        # Mock IntegrityError
        error = IntegrityError(
            "duplicate key",
            "INSERT INTO categories",
            "uq_user_category_name"
        )
        error.orig = MagicMock()
        error.orig.__str__ = MagicMock(return_value="uq_user_category_name")

        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock(side_effect=error)
        mock_db.rollback = AsyncMock()

        try:
            await service.create_category(user_id, category_data)
        except ValueError as e:
            # Check that the exception was raised with proper chaining
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, IntegrityError)
            assert "uq_user_category_name" in str(e.__cause__.orig)

    @pytest.mark.asyncio
    async def test_update_category_exception_chaining_service(self) -> None:
        """Test that update service method properly chains IntegrityError."""
        mock_db = AsyncMock()
        service = CategoryService(mock_db)
        category_id = uuid4()
        user_id = uuid4()
        category_update = CategoryUpdate(name="Updated")

        # Mock existing category
        mock_category = MagicMock()
        mock_category.id = category_id
        mock_category.user_id = user_id

        # Mock IntegrityError
        error = IntegrityError(
            "duplicate key",
            "UPDATE categories",
            "uq_user_category_name"
        )
        error.orig = MagicMock()
        error.orig.__str__ = MagicMock(return_value="uq_user_category_name")

        with patch.object(service, 'get_category', return_value=mock_category):
            mock_db.commit = AsyncMock(side_effect=error)
            mock_db.rollback = AsyncMock()

            try:
                await service.update_category(category_id, user_id, category_update)
            except ValueError as e:
                # Check that the exception was raised with proper chaining
                assert e.__cause__ is not None
                assert isinstance(e.__cause__, IntegrityError)
                assert "uq_user_category_name" in str(e.__cause__.orig)

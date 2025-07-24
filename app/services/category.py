"""Category service layer for business logic."""
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service for category operations."""

    def __init__(self, db: AsyncSession):
        """Initialize the service with database session."""
        self.db = db

    async def create_category(
        self,
        user_id: UUID,
        category_data: CategoryCreate
    ) -> Category:
        """Create a new category."""
        # Check for duplicate name is handled by database constraint
        category = Category(
            user_id=user_id,
            **category_data.model_dump(exclude_unset=True)
        )

        try:
            self.db.add(category)
            await self.db.commit()
            await self.db.refresh(category)
            return category
        except IntegrityError as e:
            await self.db.rollback()
            if "uq_user_category_name" in str(e.orig):
                raise ValueError("A category with this name already exists") from e
            raise

    async def get_category(
        self,
        category_id: UUID,
        user_id: UUID
    ) -> Category | None:
        """Get a specific category by ID."""
        query = select(Category).where(
            and_(
                Category.id == category_id,
                Category.user_id == user_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_categories(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Category], int]:
        """Get all categories for a user with pagination and filtering."""
        # Base query
        query = select(Category).where(Category.user_id == user_id)

        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.where(Category.name.ilike(search_term))

        # Count total before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Apply sorting
        sort_column = getattr(Category, sort_by, Category.created_at)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        result = await self.db.execute(query)
        categories = result.scalars().all()

        return list(categories), total

    async def update_category(
        self,
        category_id: UUID,
        user_id: UUID,
        category_data: CategoryUpdate
    ) -> Category | None:
        """Update a category."""
        category = await self.get_category(category_id, user_id)
        if not category:
            return None

        update_data = category_data.model_dump(exclude_unset=True)

        try:
            # Update fields
            for field, value in update_data.items():
                setattr(category, field, value)

            await self.db.commit()
            await self.db.refresh(category)
            return category
        except IntegrityError as e:
            await self.db.rollback()
            if "uq_user_category_name" in str(e.orig):
                raise ValueError("A category with this name already exists") from e
            raise

    async def delete_category(
        self,
        category_id: UUID,
        user_id: UUID
    ) -> bool:
        """Delete a category (hard delete)."""
        category = await self.get_category(category_id, user_id)
        if not category:
            return False

        # Hard delete - SQLAlchemy will handle setting todo.category_id to NULL
        await self.db.delete(category)
        await self.db.commit()
        return True

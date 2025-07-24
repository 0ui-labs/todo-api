"""Todo service layer for business logic."""
from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.todo import Todo, TodoStatus
from app.schemas.todo import TodoCreate, TodoFilter, TodoSort, TodoUpdate
from app.services.category import CategoryService
from app.services.tag import TagService


class TodoService:
    """Service for todo operations."""

    def __init__(self, db: AsyncSession):
        """Initialize the service with database session."""
        self.db = db

    async def create_todo(self, user_id: UUID, todo_data: TodoCreate) -> Todo | None:
        """Create a new todo."""
        # NEW: Validate category if provided
        if todo_data.category_id:
            # Use existing CategoryService to check ownership
            category_service = CategoryService(self.db)
            category = await category_service.get_category(
                category_id=todo_data.category_id,
                user_id=user_id
            )
            if not category:
                # Return None to let the API endpoint handle 404
                return None

        # Extract tag_ids before creating the todo
        tag_ids = todo_data.tag_ids if hasattr(todo_data, 'tag_ids') else []
        
        # Create todo without tag_ids
        todo_dict = todo_data.model_dump(exclude_unset=True)
        todo_dict.pop('tag_ids', None)
        
        todo = Todo(
            user_id=user_id,
            **todo_dict
        )
        
        # Handle tags if provided
        if tag_ids:
            tag_service = TagService(self.db)
            tags = await tag_service.get_by_ids(tag_ids)
            todo.tags = tags
        
        self.db.add(todo)
        await self.db.commit()

        # NEW: Return with eager loaded data
        return await self.get_todo(todo.id, user_id)

    async def get_todo(self, todo_id: UUID, user_id: UUID) -> Todo | None:
        """Get a specific todo by ID."""
        query = (
            select(Todo)
            .options(selectinload(Todo.category))
            .options(selectinload(Todo.tags))
            .where(
                and_(
                    Todo.id == todo_id,
                    Todo.user_id == user_id,
                    Todo.deleted_at.is_(None)
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_todos(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        filter_params: TodoFilter | None = None,
        sort_params: TodoSort | None = None,
    ) -> tuple[list[Todo], int]:
        """Get all todos for a user with pagination and filtering."""
        # Base query
        query = (
            select(Todo)
            .options(selectinload(Todo.category))
            .options(selectinload(Todo.tags))
            .where(
                and_(
                    Todo.user_id == user_id,
                    Todo.deleted_at.is_(None)
                )
            )
        )

        # Apply filters
        if filter_params:
            if filter_params.status:
                query = query.where(Todo.status == filter_params.status)
            if filter_params.category_id:
                query = query.where(Todo.category_id == filter_params.category_id)
            if filter_params.search:
                search_term = f"%{filter_params.search}%"
                query = query.where(
                    or_(
                        Todo.title.ilike(search_term),
                        Todo.description.ilike(search_term)
                    )
                )

        # Count total before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        # Apply sorting
        if sort_params:
            sort_column = getattr(Todo, sort_params.sort_by)
            if sort_params.order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(Todo.created_at.desc())

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        result = await self.db.execute(query)
        todos = result.scalars().all()

        return list(todos), total

    async def update_todo(
        self,
        todo_id: UUID,
        user_id: UUID,
        todo_data: TodoUpdate
    ) -> Todo | None:
        """Update a todo."""
        todo = await self.get_todo(todo_id, user_id)
        if not todo:
            return None

        update_data = todo_data.model_dump(exclude_unset=True)
        
        # Handle tags separately
        tag_ids = update_data.pop('tag_ids', None)
        
        # Handle status change to completed
        if update_data.get("status") == TodoStatus.COMPLETED and not todo.completed_at:
            update_data["completed_at"] = datetime.now()
        elif update_data.get("status") != TodoStatus.COMPLETED:
            update_data["completed_at"] = None

        # Update fields
        for field, value in update_data.items():
            setattr(todo, field, value)
            
        # Update tags if provided
        if tag_ids is not None:
            tag_service = TagService(self.db)
            tags = await tag_service.get_by_ids(tag_ids)
            todo.tags = tags

        await self.db.commit()

        # Re-query with eager loading (most reliable)
        refreshed_todo = await self.get_todo(todo_id, user_id)
        return refreshed_todo

    async def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Soft delete a todo."""
        todo = await self.get_todo(todo_id, user_id)
        if not todo:
            return False

        todo.deleted_at = datetime.now()
        await self.db.commit()
        return True

    async def get_todos_by_category(
        self,
        user_id: UUID,
        category_id: UUID
    ) -> list[Todo]:
        """Get all todos for a specific category."""
        query = (
            select(Todo)
            .where(
                and_(
                    Todo.user_id == user_id,
                    Todo.category_id == category_id,
                    Todo.deleted_at.is_(None)
                )
            )
            .order_by(Todo.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

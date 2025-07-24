"""Admin API endpoints for system management."""


from fastapi import APIRouter, HTTPException, Request, status

from app.dependencies import CurrentUser, DatabaseSession
from app.middleware.rate_limit import RateLimiters
from app.schemas.admin import LockedAccount, UnlockAccountRequest, UnlockAccountResponse
from app.services.login_rate_limit import LoginRateLimitService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/locked-accounts",
    response_model=list[LockedAccount],
    summary="Get locked accounts",
    description="Get list of all currently locked accounts (admin only)",
)
@RateLimiters.admin_list
async def get_locked_accounts(
    request: Request,
    current_user_id: CurrentUser,
    db: DatabaseSession,
) -> list[LockedAccount]:
    """Get all currently locked accounts."""
    # Get user object to check admin status
    from app.models.user import User
    user = await db.get(User, current_user_id)

    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )

    rate_limit_service = LoginRateLimitService()
    try:
        locked_accounts = await rate_limit_service.get_locked_accounts()

        return [
            LockedAccount(
                email=account["email"],
                locked_until=account["locked_until"],
                failed_attempts=account["failed_attempts"]
            )
            for account in locked_accounts
        ]
    finally:
        await rate_limit_service.close()


@router.post(
    "/unlock-account",
    response_model=UnlockAccountResponse,
    summary="Unlock user account",
    description="Manually unlock a locked user account (admin only)",
)
@RateLimiters.admin_action
async def unlock_account(
    request: Request,
    unlock_request: UnlockAccountRequest,
    current_user_id: CurrentUser,
    db: DatabaseSession,
) -> UnlockAccountResponse:
    """Unlock a locked user account."""
    # Get user object to check admin status
    from app.models.user import User
    user = await db.get(User, current_user_id)

    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )

    rate_limit_service = LoginRateLimitService()
    try:
        was_unlocked = await rate_limit_service.unlock_account(unlock_request.email)

        if was_unlocked:
            return UnlockAccountResponse(
                success=True,
                message=f"Account {unlock_request.email} has been unlocked"
            )
        else:
            return UnlockAccountResponse(
                success=False,
                message=f"Account {unlock_request.email} was not locked"
            )
    finally:
        await rate_limit_service.close()

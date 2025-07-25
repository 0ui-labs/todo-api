"""Custom exceptions for service layer."""

from datetime import datetime


class AuthServiceError(Exception):
    """Base exception for AuthService."""
    pass


class InvalidCredentialsError(AuthServiceError):
    """Raised when authentication fails due to wrong email or password."""
    def __init__(self, message: str, remaining_attempts: int, failed_attempts: int):
        self.remaining_attempts = remaining_attempts
        self.failed_attempts = failed_attempts
        super().__init__(message)


class AccountLockedError(AuthServiceError):
    """Raised when a login attempt is made on a locked account."""
    def __init__(
        self,
        message: str,
        locked_until: datetime,
        remaining_seconds: int,
        failed_attempts: int
    ):
        self.locked_until = locked_until
        self.remaining_seconds = remaining_seconds
        self.failed_attempts = failed_attempts
        super().__init__(message)

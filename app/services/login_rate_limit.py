"""Login attempt rate limiting service with exponential backoff."""

import logging
from datetime import datetime, timedelta

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.config import settings
from app.redis import get_redis_client

logger = logging.getLogger(__name__)


class LoginRateLimitService:
    """Service for rate limiting login attempts with exponential backoff."""

    def __init__(self, redis_client: redis.Redis | None = None):
        """Initialize the login rate limit service.

        Args:
            redis_client: Optional Redis client instance. If not provided,
                         creates a new one from settings.
        """
        self._redis = redis_client
        self._prefix = "failed_attempts:"
        self._lockout_prefix = "account_locked:"

        # Configuration
        self.max_attempts = 5  # Maximum failed attempts before lockout
        self.base_lockout_minutes = 1  # Base lockout time in minutes
        self.max_lockout_minutes = 480  # Maximum lockout time (8 hours)
        self.attempt_window_hours = 24  # Time window for counting attempts

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._redis is None:
            self._redis = await get_redis_client(settings.redis_db)
        return self._redis

    async def record_failed_attempt(self, email: str) -> tuple[int, datetime | None]:
        """Record a failed login attempt for a user.

        Args:
            email: The user's email address

        Returns:
            Tuple of (current_attempt_count, lockout_until_datetime)
        """
        try:
            client = await self._get_redis()
            key = f"{self._prefix}{email}"
            lockout_key = f"{self._lockout_prefix}{email}"

            # Check if account is currently locked
            locked_until = await client.get(lockout_key)
            if locked_until:
                locked_until_dt = datetime.fromisoformat(locked_until)
                if locked_until_dt > datetime.utcnow():
                    # Still locked
                    attempt_count = await client.get(key) or "0"
                    return int(attempt_count), locked_until_dt
                else:
                    # Lock expired, clear it
                    await client.delete(lockout_key)

            # Increment failed attempt counter
            current_attempts = await client.incr(key)

            # Set expiry on first attempt
            if current_attempts == 1:
                await client.expire(key, int(self.attempt_window_hours * 3600))

            # Check if we need to lock the account
            if current_attempts >= self.max_attempts:
                # Calculate lockout duration with exponential backoff
                # Attempts 5, 10, 15, 20... result in 1, 2, 4, 8... minutes
                lockout_multiplier = 2 ** (
                    (current_attempts - self.max_attempts) // self.max_attempts
                )
                lockout_minutes = min(
                    self.base_lockout_minutes * lockout_multiplier,
                    self.max_lockout_minutes
                )

                lockout_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)

                # Store lockout timestamp
                await client.setex(
                    lockout_key,
                    int(lockout_minutes * 60),
                    lockout_until.isoformat()
                )

                logger.warning(
                    f"Account {email} locked for {lockout_minutes} minutes "
                    f"after {current_attempts} failed attempts"
                )

                return current_attempts, lockout_until

            return current_attempts, None

        except (RedisError, OSError, ConnectionError) as e:
            logger.error(f"Redis error in record_failed_attempt: {e}")
            # In case of Redis failure, don't block login attempts
            # But log the issue for monitoring
            logger.warning(
                f"Unable to record failed login attempt for {email} due to Redis error"
            )
            return 0, None

    async def check_rate_limit(self, email: str) -> tuple[bool, datetime | None, int]:
        """Check if a user is allowed to attempt login.

        Args:
            email: The user's email address

        Returns:
            Tuple of (is_allowed, lockout_until_datetime, current_attempts)
        """
        try:
            client = await self._get_redis()
            lockout_key = f"{self._lockout_prefix}{email}"
            attempts_key = f"{self._prefix}{email}"

            # Check if account is locked
            locked_until = await client.get(lockout_key)
            if locked_until:
                locked_until_dt = datetime.fromisoformat(locked_until)
                if locked_until_dt > datetime.utcnow():
                    # Still locked
                    current_attempts = await client.get(attempts_key) or "0"
                    return False, locked_until_dt, int(current_attempts)
                else:
                    # Lock expired, clear it
                    await client.delete(lockout_key)

            # Get current attempt count
            current_attempts = await client.get(attempts_key) or "0"
            return True, None, int(current_attempts)

        except (RedisError, OSError, ConnectionError) as e:
            logger.error(f"Redis error in check_rate_limit: {e}")
            # In case of Redis failure, allow login attempts
            # This prevents Redis issues from completely blocking login
            return True, None, 0

    async def clear_failed_attempts(self, email: str) -> None:
        """Clear failed login attempts after successful login.

        Args:
            email: The user's email address
        """
        try:
            client = await self._get_redis()
            key = f"{self._prefix}{email}"
            lockout_key = f"{self._lockout_prefix}{email}"

            # Clear both failed attempts and any lockout
            await client.delete(key, lockout_key)

            logger.info(f"Cleared failed login attempts for {email}")

        except (RedisError, OSError, ConnectionError) as e:
            logger.error(f"Redis error in clear_failed_attempts: {e}")
            # Log but don't fail - successful login should not be blocked
            # by Redis issues

    async def unlock_account(self, email: str) -> bool:
        """Manually unlock a locked account (admin function).

        Args:
            email: The user's email address

        Returns:
            True if account was locked and is now unlocked, False otherwise
        """
        try:
            client = await self._get_redis()
            lockout_key = f"{self._lockout_prefix}{email}"
            attempts_key = f"{self._prefix}{email}"

            # Check if account was locked
            was_locked = await client.exists(lockout_key)

            # Clear both lockout and attempts
            await client.delete(lockout_key, attempts_key)

            if was_locked:
                logger.info(f"Account {email} manually unlocked by admin")
                return True
            return False

        except RedisError as e:
            logger.error(f"Redis error in unlock_account: {e}")
            return False

    async def get_locked_accounts(self) -> list[dict]:
        """Get list of currently locked accounts (admin function).

        Returns:
            List of dictionaries with email and lockout expiry information
        """
        try:
            client = await self._get_redis()
            locked_accounts = []

            # Scan for all lockout keys
            cursor = 0
            while True:
                cursor, keys = await client.scan(
                    cursor,
                    match=f"{self._lockout_prefix}*",
                    count=100
                )

                for key in keys:
                    email = key.replace(self._lockout_prefix, "")
                    locked_until = await client.get(key)
                    if locked_until:
                        locked_until_dt = datetime.fromisoformat(locked_until)
                        if locked_until_dt > datetime.utcnow():
                            # Get attempt count
                            attempts_key = f"{self._prefix}{email}"
                            attempts = await client.get(attempts_key) or "0"

                            locked_accounts.append({
                                "email": email,
                                "locked_until": locked_until_dt,
                                "failed_attempts": int(attempts)
                            })

                if cursor == 0:
                    break

            return locked_accounts

        except RedisError as e:
            logger.error(f"Redis error in get_locked_accounts: {e}")
            return []

    async def close(self) -> None:
        """Close the Redis connection."""
        if self._redis:
            await self._redis.close()

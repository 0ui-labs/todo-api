#!/usr/bin/env python3
"""Generate secure SECRET_KEY for Todo API."""
import secrets


def generate_key(length: int = 64) -> str:
    """Generate cryptographically secure key."""
    return secrets.token_urlsafe(length)


def main():
    print("🔐 Todo API Secret Key Generator")
    print("-" * 40)

    key = generate_key()

    print(f"\nGenerated SECRET_KEY:\n{key}\n")
    print("Add to your .env file:")
    print(f'SECRET_KEY="{key}"')
    print("\n⚠️  Keep this key secret and secure!")


if __name__ == "__main__":
    main()

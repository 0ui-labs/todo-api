#!/usr/bin/env python3
"""Generate secure SECRET_KEY for Todo API."""
import secrets


def generate_key(length: int = 64) -> str:
    """Generate cryptographically secure key.
    
    The key will have high entropy with many unique characters,
    meeting the API's requirement of at least 16 unique characters.
    """
    return secrets.token_urlsafe(length)


def main():
    print("🔐 Todo API Secret Key Generator")
    print("-" * 40)

    key = generate_key()
    unique_chars = len(set(key))

    print(f"\nGenerated SECRET_KEY:\n{key}\n")
    print("✅ Key Statistics:")
    print(f"   - Length: {len(key)} characters")
    print(f"   - Unique characters: {unique_chars}")
    print(f"   - Entropy: {'High' if unique_chars >= 16 else 'Low'}")
    
    print("\nAdd to your .env file:")
    print(f'SECRET_KEY="{key}"')
    print("\n⚠️  Keep this key secret and secure!")
    print("⚠️  Never use simple patterns or dictionary words!")


if __name__ == "__main__":
    main()

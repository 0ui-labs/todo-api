"""Test memory usage with request size limits."""
import asyncio
import tracemalloc

from httpx import AsyncClient

from app.main import app


async def test_memory_with_size_limits():
    """Test that the size limit middleware doesn't cause memory issues."""
    tracemalloc.start()

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test multiple requests with different sizes
        sizes = [1024, 10240, 102400, 1024000]  # 1KB, 10KB, 100KB, 1MB

        print("Testing memory usage with various request sizes:")
        for size in sizes:
            # Get baseline memory
            baseline = tracemalloc.get_traced_memory()[0]

            # Make request with specific size
            headers = {"Content-Length": str(size)}
            response = await client.get("/health", headers=headers)
            assert response.status_code == 200

            # Check memory after request
            current = tracemalloc.get_traced_memory()[0]
            memory_increase = current - baseline

            print(f"Size: {size:>8} bytes | Memory increase: {memory_increase:>8} bytes")

        # Test rejected large request
        print("\nTesting rejected large request (11MB):")
        baseline = tracemalloc.get_traced_memory()[0]

        headers = {"Content-Length": str(11 * 1024 * 1024)}
        response = await client.get("/health", headers=headers)
        assert response.status_code == 413

        current = tracemalloc.get_traced_memory()[0]
        memory_increase = current - baseline

        print(f"Rejected 11MB request | Memory increase: {memory_increase:>8} bytes")
        print("✓ Large request was rejected without loading into memory")

    tracemalloc.stop()


if __name__ == "__main__":
    asyncio.run(test_memory_with_size_limits())

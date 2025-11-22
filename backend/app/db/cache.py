from typing import Any, Optional
import json
import redis.asyncio as redis
from loguru import logger

from app.core.config import settings


class CacheManager:
    """Manager for Dragonfly (Redis-compatible) cache operations."""

    def __init__(self) -> None:
        self.client: Optional[redis.Redis] = None
        self._initialized = False

    async def connect(self) -> None:
        """Establish connection to Dragonfly."""
        try:
            self.client = await redis.from_url(
                settings.dragonfly_url,
                encoding="utf-8",
                decode_responses=True,
            )

            # Test connection
            await self.client.ping()

            self._initialized = True
            logger.info("Dragonfly connection established successfully")

        except Exception as e:
            logger.error(f"Failed to connect to Dragonfly: {e}")
            raise

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if not provided)

        Returns:
            True if successful
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        try:
            ttl = ttl or settings.cache_ttl
            serialized = json.dumps(value)
            await self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete key from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        try:
            result = await self.client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        try:
            result = await self.client.exists(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.

        Args:
            pattern: Key pattern (e.g., "claim:*")

        Returns:
            Number of keys deleted
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                return await self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache invalidate pattern error for {pattern}: {e}")
            return 0

    async def get_or_set(
        self,
        key: str,
        factory: Any,
        ttl: Optional[int] = None,
    ) -> Any:
        """
        Get value from cache or compute and cache it.

        Args:
            key: Cache key
            factory: Async function to compute value if not cached
            ttl: Time to live in seconds

        Returns:
            Cached or computed value
        """
        value = await self.get(key)

        if value is not None:
            return value

        # Compute value
        if callable(factory):
            value = await factory() if hasattr(factory, "__await__") else factory()
        else:
            value = factory

        await self.set(key, value, ttl)
        return value

    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment a counter.

        Args:
            key: Counter key
            amount: Amount to increment by

        Returns:
            New counter value
        """
        if not self.client:
            raise RuntimeError("Cache client not initialized")

        return await self.client.incrby(key, amount)

    async def disconnect(self) -> None:
        """Close Dragonfly connection."""
        if self.client:
            await self.client.aclose()
            self._initialized = False
            logger.info("Dragonfly connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if cache is connected."""
        return self._initialized and self.client is not None


# Global instance
cache_manager = CacheManager()

from redis.asyncio import Redis, ConnectionPool
from .base import Storage
from typing import List, Any, Optional

class RedisTCPStorage(Storage):
    """Classic TCP Redis for long-running servers."""

    def __init__(self, url: str):
        self.pool = ConnectionPool.from_url(url, decode_responses=True)
        self.redis = Redis(connection_pool=self.pool)

    async def execute_script(self, script: str, keys: List[str], args: List[Any]) -> List[Any]:
        return await self.redis.eval(script, len(keys), *keys, *args)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        await self.redis.set(key, value, ex=ex)

    async def close(self) -> None:
        await self.redis.aclose()
        await self.pool.disconnect()


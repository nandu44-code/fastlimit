from upstash_redis import redis as upstash_redis
from .base import Storage
from  typing  import List, Any, Optional

class UpstashHttpStorage(Storage):
    """Upstash redis for serverless architecture."""

    def __init__(self):
        pass

    async def execute_script(self, script, keys, args):
        return await self.redis.eval(script, keys, args)
    
    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)
    
    async def set(self, key:str,value: Any, ex: Optional[int] = None ) -> None :
        await self.redis.set(key, value, ex=ex)
    
    async def close(self)-> None:
        pass
    

            

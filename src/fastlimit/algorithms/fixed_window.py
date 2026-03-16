from .base import RateLimitAlgorithm
from typing import List,Any

class FixedWindow(RateLimitAlgorithm):
    """
    Classic fixed window counter: resets exactly at window boundaries

    """
    def __init__(self, limit:int = 100, window_seconds: int = 60):
        
        if limit <= 0 or window_seconds <= 0:
            raise ValueError ("Fixed window parameters must be positive")
        
        self.limit = limit
        self.window_seconds = window_seconds

    def name(self) -> str:
        return "fixed window"
    
    def get_keys(self, key:str) -> List[str]:
        return [f"count:{key}"]
    
    def get_lua_script(self):

        return """
        local count_key = KEYS[1]
        local limit     = tonumber(ARGV[1])
        local window    = tonumber(ARGV[2])

        local count = redis.call('INCR', count_key)
        if count == 1 then
            redis.call('EXPIRE', count_key, window)
        end

        local ttl = redis.call('TTL', count_key)
        if count > limit then
            return {0, 0, ttl * 1000, ttl * 1000}
        end

        return {1, limit - count, ttl * 1000, 0}
        """
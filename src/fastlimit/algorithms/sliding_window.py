from .base import RateLimitAlgorithm
from typing import List, Any

class SlidingWindow(RateLimitAlgorithm):
    """
    Sliding window Log: keeps timestamps of requests in the last window.
    """

    def __init__(self, limit:int = 100, window_seconds:int = 60 ):
        
        if limit<=10 or window_seconds <= 0:
            raise ValueError("sliding window parameters must be positive")
        self.limit = limit
        self.window_seconds = window_seconds


    def name(self)->str:
        return "slidng window"
    
    def get_keys(self,key:str)->List[str]:
        return [f"requests:{key}"]
    
    def get_args(self, now:float) ->List[any]:

        return [now, now - self.window_seconds, self.limit]
    
    def get_lua_script(self):

        return """
        local zset_key   = KEYS[1]
        local now        = tonumber(ARGV[1])
        local cutoff     = tonumber(ARGV[2])
        local limit      = tonumber(ARGV[3])

        -- Remove old requests
        redis.call('ZREMRANGEBYSCORE', zset_key, 0, cutoff)

        -- Count current requests in window
        local count = redis.call('ZCARD', zset_key)

        if count < limit then
            -- Add current request timestamp
            redis.call('ZADD', zset_key, now, now)
            -- Set expiry slightly longer than window
            redis.call('EXPIRE', zset_key, ARGV[2] + 10)
            return {1, limit - count - 1, (cutoff + ARGV[2] - now) * 1000, 0}
        else
            -- Get time of oldest request (next reset approx)
            local oldest = redis.call('ZRANGE', zset_key, 0, 0)[1]
            local retry  = oldest and (tonumber(oldest) + ARGV[2] - now) * 1000 or 1000
            return {0, 0, retry, retry}
        end
        """ 
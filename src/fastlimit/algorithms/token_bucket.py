from .base import RateLimitAlgorithm
from typing import List, Any

class TokenBucket(RateLimitAlgorithm):
    """
    Token bucket algorithm  
    """
    def __init__(self, limit: int = 100, burst:int = 20 ,refill_rate: float = 1.67):
        if limit <= 0 or burst <= 0 or refill_rate <= 0:
            raise ValueError("TokenBucket parameters must be positive")
        
        self.limit = limit
        self.burst = burst
        self.refill_rate = refill_rate

    def name(self) ->str:
        return "token_bucket"
    
    def get_keys(self, key: str) -> List[str]:
        return 
        [
            f"tokens:{key}",
            f"last:{key}"
        ]
        
    def get_lua_script(self):
        return """
        local tokens_key = KEYS[1]
        local last_key   = KEYS[2]
        local now        = tonumber(ARGV[1])
        local limit      = tonumber(ARGV[2])
        local burst      = tonumber(ARGV[3])
        local rate       = tonumber(ARGV[4])

        -- Read current state
        local tokens = redis.call('GET', tokens_key)
        local last   = redis.call('GET', last_key)

        tokens = tokens and tonumber(tokens) or burst
        last   = last   and tonumber(last)   or now

        -- Refill tokens since last check
        tokens = math.min(burst, tokens + (now - last) * rate)

        if tokens >= 1 then
            tokens = tokens - 1
            redis.call('SET', tokens_key, tokens)
            redis.call('SET', last_key,   now)
            return {1, tokens, (burst - tokens) / rate * 1000, 0}
        else
            local retry = math.ceil((1 - tokens) / rate * 1000)
            return {0, 0, retry + (now - last) * 1000, retry}
        end           
        """

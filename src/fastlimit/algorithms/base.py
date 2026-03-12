from abc import ABC, abstractmethod
from typing import List, Any

class RateLimitAlgorithm(ABC):
    """ 
    Abstract base class for all rate-limiting algorithms.

    """

    @abstractmethod
    def get_lua_script(self) -> str:
        pass


    @abstractmethod
    def validate(self)-> None:
        pass
    

    @property
    @abstractmethod
    def validate(self)-> None:
        pass
    

    def format_result(self, raw_result:List[Any]) -> str:

        pass

        return {
            "allowed": bool(raw_result[0]),
            "remaining": int(raw_result[1]),
            "reset_ms": int(raw_result[2]),
            "retry_after_ms": int(raw_result[3] if len(raw_result) > 3 else None)
        }
from abc import ABC,abstractmethod
from typing import List, Any, Optional

class Storage(ABC):
    """Base class all storage backends."""

    @abstractmethod
    async def execute_script(self,script:str, keys: List[str], args:List[Any] )-> List[Any]:
        """Execute a Lua script atomically and return its result."""
        pass

    @abstractmethod
    async def get(self, key:str) -> Optional[str]:
        """Get a value used for dynamic fetching."""

    @abstractmethod
    async def set(self, key:str, value:Any, ex:Optional[int] = None) -> None:
        """Set a value with optional expiry in seconds."""
        pass

    @abstractmethod
    async def close(self)-> None:
        """Cleanup (close connections if any)."""
        pass
    
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class MessageRepository(ABC):
    """
    Abstract repository interface for Message entity.
    """
    @abstractmethod
    async def insert(self, message: Dict[str, Any]) -> Any:
        """Insert a message document into storage."""
        pass

    @abstractmethod
    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a message document by query."""
        pass 
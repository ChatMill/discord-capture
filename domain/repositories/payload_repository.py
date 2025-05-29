from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class PayloadRepository(ABC):
    """
    Abstract repository interface for Payload entity.
    """
    @abstractmethod
    async def insert(self, payload: Dict[str, Any]) -> Any:
        """Insert a payload document into storage."""
        pass

    @abstractmethod
    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a payload document by query."""
        pass 
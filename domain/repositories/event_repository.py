from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class EventRepository(ABC):
    """
    Abstract repository interface for Event entity.
    """

    @abstractmethod
    async def insert(self, event: Dict[str, Any]) -> Any:
        """Insert an event document into storage."""
        pass

    @abstractmethod
    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find an event document by query."""
        pass

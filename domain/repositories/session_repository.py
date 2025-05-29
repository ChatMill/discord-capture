from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class SessionRepository(ABC):
    """
    Abstract repository interface for Session entity.
    """
    @abstractmethod
    async def insert(self, session: Dict[str, Any]) -> Any:
        """Insert a session document into storage."""
        pass

    @abstractmethod
    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a session document by query."""
        pass 
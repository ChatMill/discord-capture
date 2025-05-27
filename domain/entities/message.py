from dataclasses import dataclass
from typing import Any

@dataclass
class Message:
    """
    Domain entity representing a Discord message.
    """
    id: int
    content: str
    author_id: int
    author_name: str
    timestamp: Any  # Can be datetime or str, depending on usage 
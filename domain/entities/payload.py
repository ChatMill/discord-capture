from typing import List, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    """
    Abstract base class for all payloads handled by agents.
    """
    chatmill_id: str
    external_id: Optional[str]
    message_ids: List[str]

from abc import ABC
from typing import List, Optional


class Payload(ABC):
    """
    Abstract base class for all payloads handled by agents.
    """

    def __init__(self, external_id: Optional[str], message_ids: List[str]):
        self.external_id = external_id
        self.message_ids = message_ids

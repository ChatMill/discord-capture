from abc import ABC
from enum import Enum
from typing import List

from domain.entities.payload import Payload


class EventType(str, Enum):
    """
    Enum for all event types.
    """
    CAPTURE = "capture"
    SUPPLEMENT_REQUEST = "supplement_request"
    SUPPLEMENT_RESPONSE = "supplement_response"
    PUBLISH = "publish"
    PUBLISH_RESULT = "publish_result"


class Event(ABC):
    """
    Abstract base class for all domain events.
    """

    def __init__(
            self,
            event_type: str,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Payload,
            history: List[str]
    ):
        self.event_type = event_type
        self.session_id = session_id
        self.event_id = event_id
        self.operator_id = operator_id
        self.payload = payload
        self.history = history

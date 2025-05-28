from enum import Enum
from typing import List

from pydantic import BaseModel

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


class Event(BaseModel):
    """
    Base class for all domain events.
    """
    event_type: EventType
    session_id: str
    event_id: str
    operator_id: str
    payload: Payload
    history: List[str]

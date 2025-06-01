from typing import List

from pydantic import BaseModel

from domain.entities.spec import Spec
from domain.events.base_event import Event, EventType


class SupplementRequest(Event, BaseModel):
    """
    SupplementRequest event, sent by the agent to request more information from the user.
    Inherits from Event and Pydantic BaseModel. Contains only a 'question' field in addition to the base fields.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Spec
    history: List[str]
    question: str
    event_type: EventType = EventType.SUPPLEMENT_REQUEST
    agent: str = "missspec"


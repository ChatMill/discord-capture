from typing import List

from pydantic import BaseModel

from domain.entities.message import Message
from domain.entities.task import Task
from domain.events.base_event import Event, EventType


class SupplementResponse(Event, BaseModel):
    """
    SupplementResponse event, sent by the user to provide additional information requested by the agent.
    Inherits from Event and Pydantic BaseModel. Contains a 'supplement_messages' field and a 'messages' field (list of Message entities) in addition to the base fields.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Task
    history: List[str]
    supplement_messages: List[str]
    messages: List[Message]
    event_type: EventType = EventType.SUPPLEMENT_RESPONSE
    agent: str = "missspec"

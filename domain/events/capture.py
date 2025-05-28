from typing import List
from pydantic import BaseModel
from domain.entities.task import Task
from domain.entities.message import Message
from domain.events.base_event import Event, EventType


class Capture(Event, BaseModel):
    """
    Capture event, representing the start of a requirement capture session. Inherits from Event and Pydantic BaseModel.
    Includes a list of Message entities to be sent to the agent.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Task
    history: List[str]
    messages: List[Message]
    event_type: EventType = EventType.CAPTURE

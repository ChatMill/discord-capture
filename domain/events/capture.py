from typing import List

from domain.entities.message import Message
from domain.entities.payload import Payload
from domain.events.base_event import Event, EventType


class Capture(Event):
    """
    Capture event, representing the start of a requirement capture session. Inherits from Event.
    Includes a list of Message entities to be sent to the agent.
    """

    def __init__(
            self,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Payload,
            history: List[str],
            messages: List[Message]
    ):
        super().__init__(
            event_type=EventType.CAPTURE,
            session_id=session_id,
            event_id=event_id,
            operator_id=operator_id,
            payload=payload,
            history=history
        )
        self.messages = messages

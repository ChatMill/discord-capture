from typing import List
from domain.entities.task import Task
from domain.entities.message import Message
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
            payload: Task,
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

    def to_dict(self) -> dict:
        """
        Serialize the Capture event to a dictionary for JSON serialization.
        """
        return {
            "session_id": self.session_id,
            "event_id": self.event_id,
            "operator_id": self.operator_id,
            "payload": self.payload.to_dict() if hasattr(self.payload, 'to_dict') else self.payload,
            "history": self.history,
            "messages": [m.to_dict() if hasattr(m, 'to_dict') else m for m in self.messages],
        }

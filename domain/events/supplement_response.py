from typing import List

from domain.entities.message import Message
from domain.entities.task import Task
from domain.events.base_event import Event, EventType


class SupplementResponse(Event):
    """
    SupplementResponse event, sent by the user to provide additional information requested by the agent.
    Inherits from Event. Contains a 'supplement_messages' field and a 'messages' field (list of Message entities) in addition to the base fields.
    """

    def __init__(
            self,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Task,
            history: List[str],
            supplement_messages: List[str],
            messages: List[Message]
    ):
        super().__init__(
            event_type=EventType.SUPPLEMENT_RESPONSE,
            session_id=session_id,
            event_id=event_id,
            operator_id=operator_id,
            payload=payload,
            history=history
        )
        self.supplement_messages = supplement_messages
        self.messages = messages

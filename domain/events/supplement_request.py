from typing import List

from domain.entities.payload import Payload
from domain.events.base_event import Event, EventType


class SupplementRequest(Event):
    """
    SupplementRequest event, sent by the agent to request more information from the user.
    Inherits from Event. Contains only a 'question' field in addition to the base fields.
    """

    def __init__(
            self,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Payload,
            history: List[str],
            question: str
    ):
        super().__init__(
            event_type=EventType.SUPPLEMENT_REQUEST,
            session_id=session_id,
            event_id=event_id,
            operator_id=operator_id,
            payload=payload,
            history=history
        )
        self.question = question

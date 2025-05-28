from typing import List

from domain.entities.payload import Payload
from domain.events.base_event import Event, EventType
from domain.value_objects.publish_result import PublishResult


class PublishResultEvent(Event):
    """
    PublishResultEvent, representing the result of a publish action to a target platform.
    Inherits from Event. Contains a 'result' field (PublishResult value object) in addition to the base fields.
    """

    def __init__(
            self,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Payload,
            history: List[str],
            result: PublishResult
    ):
        super().__init__(
            event_type=EventType.PUBLISH_RESULT,
            session_id=session_id,
            event_id=event_id,
            operator_id=operator_id,
            payload=payload,
            history=history
        )
        self.result = result

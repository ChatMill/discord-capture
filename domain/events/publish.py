from typing import List

from domain.entities.task import Task
from domain.events.base_event import Event, EventType


class Publish(Event):
    """
    Publish event, representing the publishing of a requirement to a target platform.
    Inherits from Event. Contains a 'platform' field in addition to the base fields.
    """

    def __init__(
            self,
            session_id: str,
            event_id: str,
            operator_id: str,
            payload: Task,
            history: List[str],
            platform: str
    ):
        super().__init__(
            event_type=EventType.PUBLISH,
            session_id=session_id,
            event_id=event_id,
            operator_id=operator_id,
            payload=payload,
            history=history
        )
        self.platform = platform

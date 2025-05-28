from typing import List
from domain.entities.payload import Payload
from domain.value_objects.source import Source


class Session:
    """
    Session entity representing a requirement capture session.
    :param history: List of event IDs (event_id) associated with this session
    """

    def __init__(
            self,
            session_id: str,
            source: Source,
            history: List[str],  # List of event IDs (event_id)
            agent: str,
            payload: Payload
    ):
        self.session_id = session_id
        self.source = source
        self.history = history  # List of event IDs (event_id)
        self.agent = agent
        self.payload = payload

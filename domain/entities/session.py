from typing import List
from pydantic import BaseModel
from domain.entities.payload import Payload
from domain.value_objects.source import Source


class Session(BaseModel):
    """
    Session entity representing a requirement capture session.
    """
    session_id: str
    source: Source
    history: List[str]  # List of event IDs (event_id)
    agent: str
    payload: Payload

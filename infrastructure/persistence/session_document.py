from typing import List
from pydantic import BaseModel

class SessionDocument(BaseModel):
    """
    Persistence model for Session, used for MongoDB storage.
    Only stores id references to related entities (payload, events, etc.), not full objects.
    This model is decoupled from the domain entity and is only used for database interaction.
    """
    session_id: str
    source: dict  # Can be further normalized if needed
    payload_id: str
    history: List[str]  # List of event_id
    agent: str 
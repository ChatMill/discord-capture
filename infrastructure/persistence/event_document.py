from typing import List
from pydantic import BaseModel

class EventDocument(BaseModel):
    """
    Persistence model for Event, used for MongoDB storage.
    Only stores id references to related entities (payload, messages, etc.), not full objects.
    This model is decoupled from the domain entity and is only used for database interaction.
    """
    event_id: str
    session_id: str
    operator_id: str
    payload_id: str
    message_ids: List[str]
    agent_profile: dict  # Can be further normalized if needed
    event_type: str
    agent: str
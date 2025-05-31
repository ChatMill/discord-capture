from pydantic import BaseModel

class PayloadDocument(BaseModel):
    """
    Persistence model for Payload, used for MongoDB storage.
    Only stores the minimal fields required for identification and reference.
    This model is decoupled from the domain entity and is only used for database interaction.
    """
    payload_id: str
    type: str  # e.g. task, checklist, content_draft, etc.
    data: dict  # All other payload-specific fields, flattened for storage 
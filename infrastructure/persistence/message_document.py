from pydantic import BaseModel

class MessageDocument(BaseModel):
    """
    Persistence model for Message, used for MongoDB storage.
    Stores all message fields为独立字段，id 改为 message_id。
    This model is decoupled from the domain entity and is only used for database interaction.
    """
    message_id: str
    author_id: str
    author_name: str
    content: str
    timestamp: str 
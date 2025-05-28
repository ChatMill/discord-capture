from pydantic import BaseModel

class Message(BaseModel):
    """
    Domain entity representing a Discord message, including author id and name.
    """
    id: str
    author_id: str
    author_name: str
    content: str
    timestamp: str 
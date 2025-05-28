from typing import Optional
from pydantic import BaseModel


class PublishResult(BaseModel):
    """
    Value object representing the result of a publish event.
    """
    status: str
    platform: str
    url: Optional[str] = None
    message: Optional[str] = None
    id: Optional[str] = None

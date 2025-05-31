from typing import Any, Optional
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """
    Standard response model for agent communication.
    Attributes:
        success (bool): Indicates whether the request was successful.
        error (Optional[str]): Error message if the request failed.
        data (Optional[Any]): Business data returned on success.
    """
    success: bool
    error: Optional[str] = None
    data: Optional[Any] = None 
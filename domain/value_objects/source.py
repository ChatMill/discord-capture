from typing import List
from pydantic import BaseModel


class Source(BaseModel):
    """
    Value object representing the source context of a session (platform, org, channel, etc.).
    """
    platform: str
    organization_id: str
    project_id: str
    message_ids: List[int]
    participants: List[str]

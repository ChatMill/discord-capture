from typing import List, Optional

from pydantic import BaseModel


class Spec(BaseModel):
    """
    Domain entity representing a spec payload for Miss Spec agent.
    """
    chatmill_id: str
    external_id: Optional[str] = None
    title: str
    description: str
    message_ids: List[int]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    storypoints: Optional[float] = None
    assignees: List[str]
    priority: str
    parent_spec: Optional[str] = None
    sub_specs: List[str] = []

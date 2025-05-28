from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    """
    Domain entity representing a task payload for Miss Spec agent.
    """
    chatmill_id: str
    external_id: Optional[str] = None
    title: str
    description: str
    message_ids: List[str]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    storypoints: Optional[float] = None
    assignees: List[str]
    priority: str
    parent_task: Optional[str] = None
    sub_tasks: List[str] = []
    history: List[str] = [] 
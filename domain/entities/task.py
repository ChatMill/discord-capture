from typing import List, Optional
from domain.entities.payload import Payload


class Task(Payload):
    """
    Task entity for Miss Spec agent, representing a structured requirement or sub-task.
    Inherits from Payload.
    """

    def __init__(
            self,
            missspec_id: str,
            external_id: Optional[str],
            title: str,
            description: str,
            message_ids: List[str],
            start_time: Optional[str] = None,
            end_time: Optional[str] = None,
            storypoints: Optional[float] = None,
            assignees: Optional[List[str]] = None,
            priority: Optional[str] = None,
            parent_task: Optional[str] = None,
            sub_tasks: Optional[List['Task']] = None,
            history: Optional[List[str]] = None
    ):
        super().__init__(external_id, message_ids)
        self.missspec_id = missspec_id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.storypoints = storypoints
        self.assignees = assignees or []
        self.priority = priority
        self.parent_task = parent_task
        self.sub_tasks = sub_tasks or []
        self.history = history or []

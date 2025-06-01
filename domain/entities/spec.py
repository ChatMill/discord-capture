from typing import List, Optional

from pydantic import BaseModel

from domain.entities.payload import Payload


class Spec(Payload, BaseModel):
    """
    Spec entity for Miss Spec agent, representing a structured requirement or sub-spec.
    Inherits from Payload and Pydantic BaseModel.
    """

    external_id: Optional[str] = None
    title: str
    description: str
    message_ids: List[str]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    storypoints: Optional[float] = None
    assignees: List[str] = []
    priority: Optional[str] = None
    parent_spec: Optional[str] = None
    sub_specs: List['Spec'] = []

from pydantic import BaseModel
from typing import List
from mock.domain.entities.task import Task
from mock.domain.value_objects.agent_profile import AgentProfile
from mock.domain.entities.message import Message

class SupplementRequest(BaseModel):
    """
    SupplementRequest event, sent by the agent to request more information from the user.
    Contains all context needed for supplement, including agent profile and messages.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Task
    history: List[str]
    question: str
    event_type: str = "supplement_request"
    agent_profile: AgentProfile
    messages: List[Message]

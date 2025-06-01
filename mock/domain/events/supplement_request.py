from typing import List

from pydantic import BaseModel

from domain.entities.message import Message
from domain.entities.spec import Spec
from domain.value_objects.agent_profile import AgentProfile


class SupplementRequest(BaseModel):
    """
    SupplementRequest event, sent by the agent to request more information from the user.
    Contains all context needed for supplement, including agent profile and messages.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Spec
    history: List[str]
    question: str
    event_type: str = "supplement_request"
    agent_profile: AgentProfile
    messages: List[Message]

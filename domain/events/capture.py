from typing import List

from pydantic import BaseModel

from domain.entities.message import Message
from domain.entities.spec import Spec
from domain.events.base_event import Event, EventType
from domain.value_objects.agent_profile import AgentProfile


class Capture(Event, BaseModel):
    """
    Capture event, representing the start of a requirement capture session. Inherits from Event and Pydantic BaseModel.
    Includes a list of Message entities to be sent to the agent, and an agent profile for webhook context.
    """
    session_id: str
    event_id: str
    operator_id: str
    payload: Spec
    history: List[str]
    messages: List[Message]
    agent_profile: AgentProfile  # Profile info for webhook echoing (avatar, webhook name, channel, guild)
    event_type: EventType = EventType.CAPTURE
    agent: str = "missspec"

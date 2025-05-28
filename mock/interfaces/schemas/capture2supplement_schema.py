import asyncio
import random
import time

from domain.entities.message import Message
from domain.entities.task import Task
from domain.events.supplement_request import SupplementRequest
from domain.value_objects.agent_profile import AgentProfile


async def build_supplement_request_from_capture(capture_event: dict) -> SupplementRequest:
    """
    Build a SupplementRequest from a capture event dict.
    Simulates AI processing delay with a random sleep between 0.5 and 1.0 seconds.
    Args:
        capture_event: The raw capture event dict
    Returns:
        SupplementRequest: The assembled supplement request
    """
    # Simulate AI processing delay
    await asyncio.sleep(random.uniform(0.5, 1.0))

    session_id = capture_event.get("session_id")
    event_id = capture_event.get("event_id")
    operator_id = capture_event.get("operator_id")
    task = capture_event.get("payload")
    history = capture_event.get("history", [])
    agent_profile = capture_event.get("agent_profile", {})
    messages = capture_event.get("messages", [])

    # Simulate AI supplement content
    now = int(time.time())
    question = f"[AI补充@{now}] Please clarify the following: "
    if messages:
        question += "; ".join([m.get("content", "") for m in messages])
    else:
        question += "No messages captured."

    return SupplementRequest(
        session_id=session_id,
        event_id=event_id + "-supplement",
        operator_id=operator_id,
        payload=Task(**task),
        history=history,
        question=question,
        agent_profile=AgentProfile(**agent_profile),
        messages=[Message(**m) for m in messages]
    )

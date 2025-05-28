import uuid
from typing import List, Optional
import discord
from domain.events.capture import Capture
from domain.entities.task import Task
from domain.entities.message import Message


def build_capture_event(
    interaction: discord.Interaction,
    message_ids: List[int],
    messages: List[Message]
) -> Capture:
    """
    Build a Capture event from raw handler data.
    Args:
        interaction: The Discord interaction that triggered the event
        message_ids: List of message IDs to capture
        messages: List of domain Message objects
    Returns:
        Capture: A fully assembled Capture event
    """
    # Generate unique identifiers
    event_id = str(uuid.uuid4())
    session_id = f"session-{interaction.guild_id}-{interaction.channel_id}"

    # Build Task payload
    task_payload = Task(
        missspec_id=f"msk-{event_id[:8]}",
        external_id=None,
        title="需求草案标题示例",
        description="需求描述示例，后续可自动生成或由用户补充",
        message_ids=[str(mid) for mid in message_ids],
        start_time=None,
        end_time=None,
        storypoints=None,
        assignees=[str(interaction.user.id)],
        priority="medium",
        parent_task=None,
        sub_tasks=[],
        history=[]
    )

    # Build and return Capture event
    return Capture(
        session_id=session_id,
        event_id=event_id,
        operator_id=str(interaction.user.id),
        payload=task_payload,
        history=[],
        messages=messages
    ) 
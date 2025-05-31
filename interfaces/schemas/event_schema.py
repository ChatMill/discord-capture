import json
from typing import List

import discord

from domain.entities.message import Message
from domain.entities.task import Task
from domain.events.capture import Capture
from domain.value_objects.agent_profile import AgentProfile
from infrastructure.platform.webhook_handler import WebhookName


def build_capture_event(
        interaction: discord.Interaction,
        messages: List[Message],
        task: Task,
        session_id: str
) -> Capture:
    """
    Build a Capture event from raw handler data and a pre-built task (payload).
    Args:
        interaction: The Discord interaction that triggered the event
        messages: List of domain Message objects
        task: The pre-built Task (payload) object
        session_id: The session id to use for the event
    Returns:
        Capture: A fully assembled Capture event
    """
    # Generate unique identifiers
    event_id = f"evt-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"

    # Build AgentProfile value object
    agent_profile = AgentProfile(
        avatar_url=getattr(interaction.client, 'avatar_url', None),
        webhook_name=WebhookName.MISSSPEC.value,
        channel_id=interaction.channel_id,
        guild_id=interaction.guild_id,
        agent_end="missspec"
    )

    # Build and return Capture event
    return Capture(
        session_id=session_id,
        event_id=event_id,
        operator_id=str(interaction.user.id),
        payload=task,
        history=[],
        messages=messages,
        agent_profile=agent_profile
    )

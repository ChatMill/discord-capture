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
    session_id = f"session-{interaction.guild_id}-{interaction.channel_id}"
    chatmill_id = f"missspec-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"
    event_id = f"evt-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"

    # Build Task payload
    task_payload = Task(
        chatmill_id=chatmill_id,
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
        payload=task_payload,
        history=[],
        messages=messages,
        agent_profile=agent_profile
    )


def build_discord_embed_from_supplement_request(supplement_request: dict) -> dict:
    """
    Build a Discord Embed payload from a SupplementRequest dict.
    All fields (including nested) are echoed as embed fields.
    Args:
        supplement_request: The SupplementRequest as dict
    Returns:
        dict: Discord embed payload
    """
    embed = {
        "title": "Supplement Request",
        "description": supplement_request.get("question", ""),
        "fields": [],
        "footer": {
            "text": f"event_type: {supplement_request.get('event_type', '')} | session_id: {supplement_request.get('session_id', '')} | event_id: {supplement_request.get('event_id', '')}"
        }
    }
    # Add all top-level fields except question/event_type/session_id/event_id (已在其他位置展示)
    skip_keys = {"question", "event_type", "session_id", "event_id"}
    for k, v in supplement_request.items():
        if k in skip_keys:
            continue
        if isinstance(v, (dict, list)):
            v_str = json.dumps(v, ensure_ascii=False, indent=2)
        else:
            v_str = str(v)
        embed["fields"].append({"name": k, "value": v_str[:1024], "inline": False})
    return embed

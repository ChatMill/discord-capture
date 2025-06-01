from domain.entities.spec import Spec
from domain.entities.session import Session
import discord
from typing import List


def build_spec_payload(interaction: discord.Interaction, message_ids: List[int]) -> Spec:
    """
    Build a Spec (payload) object from interaction and message_ids.
    Args:
        interaction: The Discord interaction that triggered the event
        message_ids: List of message IDs to capture
    Returns:
        Spec: The assembled Spec (payload) object
    """
    chatmill_id = f"missspec-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"
    spec_payload = Spec(
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
        parent_spec=None,
        sub_specs=[],
    )
    return spec_payload


def build_session(interaction: discord.Interaction) -> Session:
    """
    Build a Session object from interaction.
    Args:
        interaction: The Discord interaction that triggered the event
    Returns:
        Session: The assembled Session object
    """
    session_id = f"session-{interaction.guild_id}-{interaction.channel_id}"
    session = Session(
        session_id=session_id,
        guild_id=interaction.guild_id,
        channel_id=interaction.channel_id,
        created_by=str(interaction.user.id),
        # Add other fields as needed
    )
    return session

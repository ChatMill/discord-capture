from domain.entities.task import Task
from domain.entities.session import Session
import discord
from typing import List


def build_task_payload(interaction: discord.Interaction, message_ids: List[int]) -> Task:
    """
    Build a Task (payload) object from interaction and message_ids.
    Args:
        interaction: The Discord interaction that triggered the event
        message_ids: List of message IDs to capture
    Returns:
        Task: The assembled Task (payload) object
    """
    chatmill_id = f"missspec-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"
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
    )
    return task_payload


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

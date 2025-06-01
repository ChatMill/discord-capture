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
    user_id = str(interaction.user.id)
    now = None  # You can use datetime.now().isoformat() if you want real timestamps
    spec_payload = Spec(
        chatmill_id=chatmill_id,  # Unique identifier
        external_id=None,  # External system id
        title="需求草案标题示例",  # Title
        description="需求描述示例，后续可自动生成或由用户补充",  # Description
        message_ids=[str(mid) for mid in message_ids],  # Related message ids
        start_time=None,  # Start time
        end_time=None,  # End time
        storypoints=None,  # Effort estimation
        assignees=[user_id],  # Responsible users
        priority="medium",  # Priority
        parent_spec=None,  # Parent spec id
        sub_specs=[],  # Sub-specs
        created_at=now,  # Creation timestamp
        updated_at=now,  # Last update timestamp
        created_by=user_id,  # Creator
        updated_by=user_id,  # Last modifier
        status="open",  # Current status
        tags=[],  # Tags or labels
        attachments=[],  # Attachment URLs
        acceptance_criteria=None,  # Acceptance criteria
        comments=[],  # Comments or discussion
        related_specs=[],  # Related specs/issues
        type="feature",  # Type of spec
        actor=None,  # The actor/user role for this spec
        trigger=None,  # The trigger/event for this spec
        flow=None,  # The flow/scenario for this spec
        custom_fields=None,  # Custom fields for extensibility
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

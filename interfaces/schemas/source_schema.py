from domain.value_objects.source import Source
import discord
from typing import List, Optional


def build_source(
        interaction: discord.Interaction,
        message_ids: List[int],
        participants: Optional[List[str]] = None
) -> Source:
    """
    Build a Source value object from interaction, message_ids, and participants.
    Args:
        interaction: The Discord interaction that triggered the event
        message_ids: List of message IDs
        participants: List of participant user IDs (optional)
    Returns:
        Source: The assembled Source value object
    """
    # Example: platform/org/project可根据实际业务补充
    source = Source(
        platform="discord",
        organization_id=str(getattr(interaction.guild, 'id', '')),
        project_id=str(getattr(interaction.channel, 'id', '')),
        message_ids=message_ids,
        participants=participants or []
    )
    return source

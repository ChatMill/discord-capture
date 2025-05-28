from typing import Optional

from pydantic import BaseModel


class AgentProfile(BaseModel):
    """
    Value object representing the agent profile for Discord webhook operations.
    Includes all necessary context for sending or echoing messages via webhook.
    """
    avatar_url: Optional[str] = None  # The avatar URL to use for the webhook sender
    webhook_name: str  # The webhook name (also used as sender name)
    channel_id: int  # The Discord channel ID for message delivery
    guild_id: int  # The Discord guild (server) ID for message delivery
    capture_end: str = "discord"  # The capture end identifier, fixed as 'discord'
    agent_end: str = "missspec"  # The agent end identifier, fixed as 'missspec'

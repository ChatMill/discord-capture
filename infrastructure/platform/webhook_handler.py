from enum import Enum
from typing import Dict, Optional

import discord
import httpx

from domain.value_objects.agent_profile import AgentProfile


class WebhookName(str, Enum):
    """
    Enum for all agent webhook names.
    The value will be used as both the Discord webhook name and the sender name displayed in Discord messages.
    """
    MISSSPEC = 'Miss Spec'


# Internal cache for webhooks: {(name, channel_id): webhook_url}
_webhook_cache: Dict[tuple, str] = {}


async def set_webhook(name: str, channel_id: int, bot_client) -> str:
    """
    Create and cache a Discord webhook for the given name and channel if not already cached.
    Args:
        name: The webhook name (used as key)
        channel_id: The Discord channel ID
        bot_client: The DiscordBotClient instance (optional, will use DI if not provided)
    Returns:
        The webhook URL as a string
    """
    if (name, channel_id) in _webhook_cache:
        return _webhook_cache[(name, channel_id)]
    channel = await bot_client.fetch_channel(channel_id)
    if not isinstance(channel, discord.TextChannel):
        raise ValueError('Channel is not a text-based channel (TextChannel required)')
    webhooks = await channel.webhooks()
    webhook = next((wh for wh in webhooks if wh.name == name), None)
    if not webhook:
        webhook = await channel.create_webhook(
            name=name,
        )
    _webhook_cache[(name, channel_id)] = webhook.url
    return webhook.url


async def get_webhook_url(name: str, channel_id: int) -> Optional[str]:
    """
    Get a Discord webhook URL by name and channel_id from cache. Return None if not found.
    Args:
        name: The webhook name
        channel_id: The Discord channel ID
    Returns:
        The webhook URL as a string, or None if not found
    """
    key = (name, channel_id)
    return _webhook_cache.get(key)


async def send_webhook_message(
        agent_profile: AgentProfile,
        content: str = "",
        embeds: list = None
):
    """
    Send a message to a Discord channel via webhook, using AgentProfile for all context.
    Args:
        agent_profile: AgentProfile value object (must include webhook_name, channel_id, avatar_url, etc.)
        content: The message content to send (optional)
        embeds: List of Discord embed dicts (optional)
    Raises:
        Exception: If webhook does not exist for the given name and channel_id
    """
    webhook_name = agent_profile.webhook_name
    channel_id = agent_profile.channel_id
    avatar_url = agent_profile.avatar_url
    # Only try to get webhook URL, do not auto-create
    webhook_url = await get_webhook_url(webhook_name, channel_id)
    payload = {
        "username": webhook_name,
        "avatar_url": avatar_url,
    }
    if content:
        payload["content"] = content
    if embeds:
        payload["embeds"] = embeds
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(webhook_url, json=payload, timeout=10)
            print(f"[send_webhook_message] Sent webhook message as {webhook_name}, status={resp.status_code}")
    except Exception as e:
        print(f"[send_webhook_message] Failed to send webhook message: {e}")

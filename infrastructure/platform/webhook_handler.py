from typing import Dict
import discord
from enum import Enum
from infrastructure.platform.discord_client import DiscordBotClient
import httpx


class WebhookName(str, Enum):
    """
    Enum for all agent webhook names.
    The value will be used as both the Discord webhook name and the sender name displayed in Discord messages.
    """
    MISSSPEC = 'Miss Spec'


# Internal cache for webhooks: {(name, channel_id): webhook_url}
_webhook_cache: Dict[tuple, str] = {}


async def set_webhook(name: str, channel_id: int, bot_client: DiscordBotClient) -> str:
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
        avatar_url = getattr(bot_client, 'avatar_url', None)
        webhook = await channel.create_webhook(
            name=name,
            avatar=avatar_url
        )
    _webhook_cache[(name, channel_id)] = webhook.url
    return webhook.url


async def get_webhook_url(name: str, channel_id: int) -> str:
    """
    Get a Discord webhook URL by name and channel_id from cache. Raise if not found.
    Args:
        name: The webhook name
        channel_id: The Discord channel ID
    Returns:
        The webhook URL as a string
    Raises:
        KeyError: If the webhook is not cached
    """
    key = (name, channel_id)
    if key in _webhook_cache:
        return _webhook_cache[key]
    raise KeyError(f"Webhook for name={name} and channel_id={channel_id} not found in cache. Please call set_webhook "
                   f"first.")


async def send_webhook_message(
    name: WebhookName,
    interaction: discord.Interaction,
    content: str,
    avatar_url: str = None,
    bot_client: DiscordBotClient = None
):
    """
    Send a message to a Discord channel via webhook, using the same name for both webhook and sender username.
    Args:
        name: The webhook name (WebhookName enum, also used as sender username)
        interaction: The Discord interaction object (provides channel_id and client)
        content: The message content to send
        avatar_url: The avatar URL to use for the sender (optional)
        bot_client: DiscordBotClient instance (optional, defaults to interaction.client)
    """
    channel_id = interaction.channel_id
    client = bot_client if bot_client is not None else interaction.client
    try:
        # Try to get webhook URL from cache, otherwise create it
        try:
            webhook_url = await get_webhook_url(name, channel_id)
        except KeyError:
            webhook_url = await set_webhook(name, channel_id, client)
        # Use bot avatar if not provided
        if avatar_url is None and hasattr(client, "avatar_url"):
            avatar_url = getattr(client, "avatar_url", None)
        payload = {
            "content": content,
            "username": name,
        }
        if avatar_url:
            payload["avatar_url"] = avatar_url
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
        print(f"[send_webhook_message] Sent webhook message as {name}")
    except Exception as e:
        print(f"[send_webhook_message] Failed to send webhook message: {e}")

import discord
from interfaces.commands.discord_commands import register_commands
import httpx
from infrastructure.platform.webhook_handler import set_bot_client_instance


class DiscordBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.avatar_url = None  # Cache for bot avatar URL
        set_bot_client_instance(self)

    async def setup_hook(self):
        register_commands(self.tree)
        await self.tree.sync()
        print("Global slash commands synced")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        # Cache the bot's avatar URL
        if self.user and self.user.avatar:
            self.avatar_url = self.user.avatar.url
        else:
            self.avatar_url = None

    async def fetch_message(self, channel_id: int, message_id: int):
        """
        Fetch a single message by channel ID and message ID.
        """
        channel = self.get_channel(channel_id) or await self.fetch_channel(channel_id)
        try:
            return await channel.fetch_message(message_id)
        except Exception as e:
            print(f"[fetch_message] Failed to fetch message {message_id} in channel {channel_id}: {e}")
            return None

    async def fetch_messages(self, channel_id: int, message_ids: list[int]):
        """
        Fetch multiple messages by their IDs from a given channel.
        """
        channel = self.get_channel(channel_id) or await self.fetch_channel(channel_id)
        results = []
        for mid in message_ids:
            try:
                msg = await channel.fetch_message(mid)
                results.append(msg)
            except Exception as e:
                print(f"[fetch_messages] Failed to fetch message {mid} in channel {channel_id}: {e}")
                results.append(None)
        return results


def send_webhook_message(
    webhook_url: str,
    content: str,
    username: str,
    avatar_url: str = None,
    client: DiscordBotClient = None
):
    """
    Send a message to a Discord channel via webhook.
    If avatar_url is None and client is provided, use the bot's avatar.
    :param webhook_url: The Discord webhook URL
    :param content: The message content to send
    :param username: The username to display as the sender
    :param avatar_url: The avatar URL to use for the sender (optional)
    :param client: DiscordBotClient instance to get default avatar (optional)
    """
    if avatar_url is None and client is not None:
        avatar_url = getattr(client, "avatar_url", None)
    payload = {
        "content": content,
        "username": username,
    }
    if avatar_url:
        payload["avatar_url"] = avatar_url
    try:
        response = httpx.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[send_webhook_message] Sent webhook message as {username}")
    except Exception as e:
        print(f"[send_webhook_message] Failed to send webhook message: {e}")

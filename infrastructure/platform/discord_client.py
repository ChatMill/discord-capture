import discord
from interfaces.commands.discord_commands import register_commands


class DiscordBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        register_commands(self.tree)
        await self.tree.sync()
        print("Global slash commands synced")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

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

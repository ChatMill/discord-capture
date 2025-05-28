import discord

from interfaces.commands.discord_commands import register_commands


class DiscordBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.avatar_url = None  # Cache for bot avatar URL

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

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Entry point for the discord-capture application.

from infrastructure.platform.discord_client import DiscordBotClient
from infrastructure.config.settings import settings
import discord

if __name__ == '__main__':
    intents = discord.Intents.default()
    client = DiscordBotClient(intents=intents)
    client.run(settings.DISCORD_TOKEN)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

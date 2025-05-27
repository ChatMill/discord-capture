# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Entry point for the discord-capture application.

import discord
from infrastructure.config.settings import settings

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == '__main__':
    intents = discord.Intents.default()
    client = MyClient(intents=intents)
    client.run(settings.DISCORD_TOKEN)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

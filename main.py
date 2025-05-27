# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Entry point for the discord-capture application.

from infrastructure.platform.discord_client import DiscordBotClient
from infrastructure.config.settings import settings
import discord
from fastapi import FastAPI
import threading
import uvicorn

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "discord-capture"}


def run_discord_bot():
    intents = discord.Intents.default()
    client = DiscordBotClient(intents=intents)
    client.run(settings.MISS_SPEC_DISCORD_TOKEN)


if __name__ == '__main__':
    # 启动 Discord Bot 线程
    threading.Thread(target=run_discord_bot, daemon=True).start()
    # 启动 FastAPI 服务
    uvicorn.run(app, host="0.0.0.0", port=8101)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

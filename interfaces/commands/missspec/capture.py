import asyncio
from typing import List, Optional

import discord
from discord import app_commands

from domain.services.message_fetcher_service import MessageFetcherService
from infrastructure.platform.discord_client import DiscordBotClient
from application.handlers.missspec.capture_handler import capture_handler


def parse_message_ids(message_ids_str: str) -> List[int]:
    """
    Parse the message_ids string, supporting only comma-separated IDs.
    Returns a list of integers.
    """
    message_ids_str = message_ids_str.replace(' ', '')
    try:
        return [int(mid) for mid in message_ids_str.split(',') if mid]
    except Exception:
        return []


def register_capture_command(tree: app_commands.CommandTree):
    @tree.command(name="capture", description="Capture fleeting ideas to make spec")
    @app_commands.describe(
        message_ids="The message IDs to capture (comma separated, e.g. 123,456,789)",
        participants="Optional participants (comma separated user mentions or IDs)"
    )
    async def capture_command(
            interaction: discord.Interaction,
            message_ids: str,
            participants: Optional[str] = None
    ):
        """
        Handle the /capture slash command for Miss Spec. Parses message_ids and participants, and replies with the parsed info.
        """
        # --- Delegate to handler, return reply ---
        await interaction.response.send_message(
            await capture_handler(interaction, message_ids, participants)
        )

from typing import List, Optional
import discord
from discord import app_commands
from application.handlers.missspec.supplement_handler import supplement_handler

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

def register_supplement_command(tree: app_commands.CommandTree):
    @tree.command(name="supplement", description="Supplement session with new messages (MissSpec)")
    @app_commands.describe(
        session_id="The session ID to supplement (optional, will auto-match by channel if not provided)",
        message_ids="The message IDs to supplement (comma separated, e.g. 123,456,789)"
    )
    async def supplement_command(
            interaction: discord.Interaction,
            message_ids: str,
            session_id: Optional[str] = None
    ):
        """
        Handle the /supplement slash command for Miss Spec. Accepts optional session_id and message_ids, replies with the parsed info.
        """
        await interaction.response.send_message(
            await supplement_handler(interaction, session_id, message_ids)
        ) 
import discord
from discord import app_commands
from typing import Optional
from application.handlers.missspec.list_message_handler import list_message_handler


def register_list_message_command(tree: app_commands.CommandTree):
    @tree.command(name="list-message", description="List all messages for a session")
    @app_commands.describe(
        session_id="The session ID to list messages for (optional, will auto-match by channel if not provided)"
    )
    async def list_message_command(
        interaction: discord.Interaction,
        session_id: Optional[str] = None
    ):
        """
        Handle the /list-message slash command for Miss Spec. Returns all messages for the given session.
        """
        result = await list_message_handler(interaction, session_id)
        if isinstance(result, list) and all(isinstance(e, discord.Embed) for e in result):
            await interaction.response.send_message(embeds=result, ephemeral=False)
        else:
            await interaction.response.send_message(str(result), ephemeral=True) 
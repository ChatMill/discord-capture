from infrastructure.config.settings import settings
from interfaces.commands.missspec import register_commands as register_missspec_commands
from discord import app_commands


def register_commands(tree: app_commands.CommandTree):
    """
    Register all available Discord slash commands for all configured bots.
    """
    # Register Miss Spec commands only if configured
    if hasattr(settings, "MISS_SPEC_DISCORD_TOKEN") and settings.MISS_SPEC_DISCORD_TOKEN:
        register_missspec_commands(tree)

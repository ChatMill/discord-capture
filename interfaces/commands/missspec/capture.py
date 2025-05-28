import discord
from discord import app_commands
from typing import List, Optional
import asyncio
from infrastructure.config.settings import settings
from domain.services.message_fetcher_service import MessageFetcherService
from interfaces.schemas.event_schema import build_capture_event
from interfaces.api.to_missspec.capture import notify_missspec_capture


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
        # Parse message_ids
        parsed_ids = parse_message_ids(message_ids)
        # Parse participants as a comma-separated string
        if participants:
            participants_list = [p.strip() for p in participants.split(',') if p.strip()]
        else:
            participants_list = []
        # Get initiator info
        initiator = interaction.user
        initiator_info = f"{initiator.display_name} (ID: {initiator.id})"

        # Fetch messages using MessageFetcherService
        channel_id = interaction.channel_id
        fetcher = MessageFetcherService(interaction.client)
        fetched_messages = await fetcher.fetch_messages(channel_id, parsed_ids)
        print(
            f"[capture] fetched messages: {[{'id': m.id, 'content': m.content, 'author': m.author_name} for m in fetched_messages]}")

        # Prepare playful, first-person reply message
        reply = (
            "✨ Got it! I've bottled up your spark of inspiration and sent it to my idea lab.\n\n"
            "Here's what I've captured:\n"
            f"• Message IDs: {parsed_ids}\n"
            f"• Participants: {participants_list if participants_list else 'None'}\n"
            f"• Initiator: {initiator_info}\n\n"
            "I'm pondering your ideas... I'll get back to you once my creative gears finish turning! 🧠💡"
        )
        print(f"[capture] message_ids={parsed_ids}, participants={participants_list}, initiator={initiator_info}")
        await interaction.response.send_message(reply)

        # --- Asynchronously notify agent mock service via HTTP POST ---
        async def notify_agent():
            try:
                # Build Capture event using schema factory
                capture_event = build_capture_event(
                    interaction=interaction,
                    message_ids=parsed_ids,
                    messages=fetched_messages,
                    participants=participants_list
                )
                # Notify Miss Spec agent
                await notify_missspec_capture(capture_event)
            except Exception as e:
                print(f"[capture] Failed to notify agent: {e}")

        # Fire and forget (non-blocking)
        asyncio.create_task(notify_agent())

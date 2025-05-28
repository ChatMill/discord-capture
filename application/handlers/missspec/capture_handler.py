from application.services.missspec.capture import handle_capture_command
from domain.services.message_fetcher_service import MessageFetcherService
from typing import Optional
import asyncio


def parse_message_ids(message_ids_str: str):
    """
    Parse the message_ids string, supporting only comma-separated IDs.
    Returns a list of integers.
    """
    message_ids_str = message_ids_str.replace(' ', '')
    try:
        return [int(mid) for mid in message_ids_str.split(',') if mid]
    except Exception:
        return []


def parse_participants(participants: Optional[str]):
    if participants:
        return [p.strip() for p in participants.split(',') if p.strip()]
    return []


async def capture_handler(interaction, message_ids: str, participants: Optional[str]):
    """
    Handler for MissSpec capture command. Parses/validates parameters, fetches messages, calls service, and returns reply.
    """
    parsed_ids = parse_message_ids(message_ids)
    participants_list = parse_participants(participants)
    channel_id = interaction.channel_id
    fetcher = MessageFetcherService(interaction.client)
    fetched_messages = await fetcher.fetch_messages(channel_id, parsed_ids)

    initiator = interaction.user
    initiator_info = f"{initiator.display_name} (ID: {initiator.id})"

    reply = (
        "✨ Got it! I've bottled up your spark of inspiration and sent it to my idea lab.\n\n"
        "Here's what I've captured:\n"
        f"• Message IDs: {parsed_ids}\n"
        f"• Participants: {participants_list if participants_list else 'None'}\n"
        f"• Initiator: {initiator_info}\n\n"
        "I'm pondering your ideas... I'll get back to you once my creative gears finish turning! 🧠💡"
    )

    # fire and forget业务链路
    asyncio.create_task(handle_capture_command(interaction, parsed_ids, fetched_messages))
    return reply

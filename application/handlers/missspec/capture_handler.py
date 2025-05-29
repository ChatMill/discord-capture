import asyncio
from typing import Optional

from application.services.missspec.capture import handle_capture_command
from domain.services.message_fetcher_service import MessageFetcherService
from interfaces.schemas.source_schema import build_source
from interfaces.schemas.payload_schema import build_task_payload
from interfaces.schemas.event_schema import build_capture_event
from interfaces.schemas.session_schema import build_session

# Assume repositories are imported and available
from infrastructure.repositories.session_repository_impl import SessionRepositoryImpl
from infrastructure.repositories.payload_repository_impl import PayloadRepositoryImpl
from infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from motor.motor_asyncio import AsyncIOMotorClient

# Example: get MongoDB client and database (in real app, use DI or FastAPI Depends)
client = AsyncIOMotorClient("mongodb://mongodb:27017")
db = client["chatmill"]
session_repo = SessionRepositoryImpl(db)
payload_repo = PayloadRepositoryImpl(db)
event_repo = EventRepositoryImpl(db)
message_repo = MessageRepositoryImpl(db)


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
    Handler for MissSpec capture command.
    Parses/validates parameters, fetches messages, assembles domain objects, stores them, and calls service.
    """
    parsed_ids = parse_message_ids(message_ids)
    participants_list = parse_participants(participants)
    channel_id = interaction.channel_id
    fetcher = MessageFetcherService(interaction.client)
    fetched_messages = await fetcher.fetch_messages(channel_id, parsed_ids)

    # Assemble domain objects
    source = build_source(interaction, parsed_ids, participants_list)
    task = build_task_payload(interaction, parsed_ids)
    event = build_capture_event(
        interaction=interaction,
        messages=fetched_messages,
        task=task
    )
    session = build_session(source, task, event)

    # Store all domain objects in MongoDB
    await session_repo.insert(session.dict())
    await payload_repo.insert(task.dict())
    await event_repo.insert(event.dict())
    await asyncio.gather(*(message_repo.insert(m.dict()) for m in fetched_messages))

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
    asyncio.create_task(handle_capture_command(interaction, event))
    return reply

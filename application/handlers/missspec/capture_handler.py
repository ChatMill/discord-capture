import asyncio
from typing import Optional

from application.services.missspec.capture import handle_capture_command
from domain.services.message_fetcher_service import MessageFetcherService
from interfaces.schemas.source_schema import build_source
from interfaces.schemas.payload_schema import build_spec_payload
from interfaces.schemas.event_schema import build_capture_event
from interfaces.schemas.session_schema import build_session
from domain.services.message_validator import MessageValidator

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
    parsed_ids = parse_message_ids(message_ids)  # List[int]
    participants_list = parse_participants(participants)
    channel_id = interaction.channel_id
    fetcher = MessageFetcherService(interaction.client)

    # 使用 CaptureMessageValidator 处理 message ids（全部用 str 参与 fetch，后续还原 int）
    str_ids = [str(mid) for mid in parsed_ids]
    fetched_messages, not_found_str_ids = await MessageValidator.fetch_and_validate(
        str_ids, fetcher, channel_id
    )
    deduped_ids = MessageValidator.deduplicate_message_ids(str_ids)
    deduped_int_ids = [int(mid) for mid in deduped_ids]
    not_found_ids = [int(mid) for mid in not_found_str_ids]
    found_ids = [int(m.id) for m in fetched_messages]

    # 生成 session_id
    session_id = f"session-{interaction.guild_id}-{interaction.channel_id}-{interaction.id}"

    # Assemble domain objects（只用 fetch 到的消息 id）
    source = build_source(interaction, found_ids, participants_list)
    spec = build_spec_payload(interaction, found_ids)
    event = build_capture_event(
        interaction=interaction,
        messages=fetched_messages,
        spec=spec,
        session_id=session_id
    )
    session = build_session(source, spec, event, session_id=session_id)

    # Store all domain objects in MongoDB
    await session_repo.insert(session)
    await payload_repo.insert(spec)
    await event_repo.insert(event)
    await asyncio.gather(*(message_repo.insert(m) for m in fetched_messages))

    initiator = interaction.user
    initiator_info = f"{initiator.display_name} (ID: {initiator.id})"

    not_found_msg = MessageValidator.format_not_found_message([str(mid) for mid in not_found_ids])
    reply = (
        "✨ Got it! I've bottled up your spark of inspiration and sent it to my idea lab.\n\n"
        "Here's what I've captured:\n"
        f"• Message IDs: {deduped_int_ids}\n"
        f"{not_found_msg}"
        f"• Participants: {participants_list if participants_list else 'None'}\n"
        f"• Initiator: {initiator_info}\n\n"
        "I'm pondering your ideas... I'll get back to you once my creative gears finish turning! 🧠💡"
    )

    # fire and forget业务链路
    asyncio.create_task(handle_capture_command(interaction, event))
    return reply

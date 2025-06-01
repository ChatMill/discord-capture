import asyncio
from typing import Optional
from application.services.missspec.supplement_service import handle_supplement_command
from domain.services.message_fetcher_service import MessageFetcherService
from interfaces.schemas.source_schema import build_source
from interfaces.schemas.payload_schema import build_spec_payload
from interfaces.schemas.event_schema import build_capture_event
from interfaces.schemas.session_schema import build_session
from domain.services.message_validator import MessageValidator
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

async def supplement_handler(interaction, session_id: Optional[str], message_ids: str):
    """
    Handler for MissSpec supplement command.
    Accepts optional session_id, fetches session by id or by channel+guild, appends event_id to history, and processes supplement logic.
    Returns: reply string for user.
    """
    parsed_ids = parse_message_ids(message_ids)  # List[int]
    channel_id = str(interaction.channel_id)
    guild_id = str(interaction.guild_id)
    fetcher = MessageFetcherService(interaction.client)
    str_ids = [str(mid) for mid in parsed_ids]
    fetched_messages, not_found_str_ids = await MessageValidator.fetch_and_validate(
        str_ids, fetcher, channel_id
    )
    deduped_ids = MessageValidator.deduplicate_message_ids(str_ids)
    deduped_int_ids = [int(mid) for mid in deduped_ids]
    not_found_ids = [int(mid) for mid in not_found_str_ids]
    found_ids = [int(m.id) for m in fetched_messages]

    # session 查找逻辑
    session = None
    if session_id:
        session = await session_repo.find({"session_id": session_id})
        if not session:
            return ("❌ Session ID is invalid or not found. Please check and try again.")
    else:
        # 用 channel_id + guild_id 查找
        sessions = await session_repo.find_many({
            "source.organization_id": guild_id,
            "source.project_id": channel_id
        })
        if len(sessions) == 0:
            return ("❌ No session found for this channel. Please start a session or specify a session ID.")
        if len(sessions) > 1:
            return ("❌ Multiple sessions found for this channel. Please specify a session ID to disambiguate.")
        session = sessions[0]
        session_id = session.session_id

    # supplement 正常流程
    source = build_source(interaction, found_ids, participants=None)
    spec = build_spec_payload(interaction, found_ids)
    event = build_capture_event(
        interaction=interaction,
        messages=fetched_messages,
        spec=spec,
        session_id=session_id
    )
    # 追加 event_id 到 history
    session.history.append(event.event_id)
    await session_repo.insert(session)
    await payload_repo.insert(spec)
    await event_repo.insert(event)
    await asyncio.gather(*(message_repo.insert(m) for m in fetched_messages))
    initiator = interaction.user
    initiator_info = f"{initiator.display_name} (ID: {initiator.id})"
    not_found_msg = MessageValidator.format_not_found_message([str(mid) for mid in not_found_ids])
    reply = (
        "✨ Supplement received! I've added your messages to the session.\n\n"
        "Here's what I've supplemented:\n"
        f"• Message IDs: {deduped_int_ids}\n"
        f"{not_found_msg}"
        f"• Initiator: {initiator_info}\n\n"
        "I'm processing your supplement... I'll get back to you once the agent responds! 🧠💡"
    )
    # fire and forget业务链路
    asyncio.create_task(handle_supplement_command(interaction, event))
    return reply 
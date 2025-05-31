import asyncio
from infrastructure.repositories.session_repository_impl import SessionRepositoryImpl
from infrastructure.repositories.event_repository_impl import EventRepositoryImpl
from motor.motor_asyncio import AsyncIOMotorClient
import discord

# MongoDB 依赖（可与 capture_handler 复用）
client = AsyncIOMotorClient("mongodb://mongodb:27017")
db = client["chatmill"]
session_repo = SessionRepositoryImpl(db)
event_repo = EventRepositoryImpl(db)

async def list_message_handler(session_id: str):
    """
    Handler for MissSpec list-message command.
    Given a session_id, returns all messages involved in the session as compact Discord embeds (one per message, minimal height).
    """
    session = await session_repo.find({"session_id": session_id})
    if not session:
        embed = discord.Embed(title="Session Not Found", description=f"Session not found: {session_id}", color=discord.Color.red())
        return [embed]
    event_ids = session.history
    # 并发查找所有 event
    events = await asyncio.gather(*[event_repo.find({"event_id": eid}) for eid in event_ids])
    all_messages = []
    for event in events:
        if event and hasattr(event, "messages") and event.messages:
            all_messages.extend(event.messages)
    # 去重（按 message.id）
    unique = {}
    for m in all_messages:
        unique[m.id] = m
    unique_messages = list(unique.values())
    if not unique_messages:
        embed = discord.Embed(title="No Messages", description=f"No messages found for session: {session_id}", color=discord.Color.orange())
        return [embed]
    # 主 embed
    main_embed = discord.Embed(title=f"Messages for session {session_id}", description=f"Total: {len(unique_messages)} messages.", color=discord.Color.blue())
    embeds = [main_embed]
    # 每条 message 一个 embed，极简高度
    for m in unique_messages:
        # 尝试解析时间
        time_str = m.timestamp
        try:
            import dateutil.parser
            dt = dateutil.parser.parse(m.timestamp)
            time_str = dt.strftime('%Y-%m-%d %H:%M')
        except Exception:
            pass
        # title=作者，description=内容+时间，所有字段一行
        desc = f"{m.content} \u2022 {time_str}"
        msg_embed = discord.Embed(title=m.author_name, description=desc, color=discord.Color.green())
        msg_embed.set_footer(text=f"ID: {m.id}")
        embeds.append(msg_embed)
    return embeds 
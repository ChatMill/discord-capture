import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from infrastructure.platform.webhook_handler import send_webhook_message
from interfaces.schemas.event_schema import build_discord_embed_from_supplement_request

router = APIRouter()


@router.post("/capture/discord/supplement_request")
async def receive_supplement_request(request: Request):
    data = await request.json()
    logging.info(f"[from_missspec] Received supplement_request: {data}")
    print(f"[from_missspec] Received supplement_request: {data}")

    # 1. 组装 Discord Embed
    embed = build_discord_embed_from_supplement_request(data)
    agent_profile = data.get("agent_profile", {})

    # 2. 发送 embed 消息到 Discord
    from domain.value_objects.agent_profile import AgentProfile
    await send_webhook_message(
        agent_profile=AgentProfile(**agent_profile),
        embeds=[embed]
    )

    return JSONResponse(content={"status": "received"}, status_code=200)

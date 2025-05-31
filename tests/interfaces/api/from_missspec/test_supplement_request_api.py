import pytest
from fastapi import Request
from fastapi.responses import JSONResponse
from interfaces.api.from_missspec import supplement_request
from unittest.mock import AsyncMock, patch, MagicMock
import types

@pytest.mark.asyncio
async def test_receive_supplement_request_success(monkeypatch):
    # 构造 request mock
    data = {
        "question": "Q?",
        "event_type": "supplement_request",
        "session_id": "sid",
        "event_id": "eid",
        "agent_profile": {
            "avatar_url": "url",
            "webhook_name": "wh",
            "channel_id": 1,
            "guild_id": 2,
            "capture_end": "discord",
            "agent_end": "missspec"
        },
        "task": {"foo": "bar"}
    }
    request = MagicMock(spec=Request)
    request.json = AsyncMock(return_value=data)
    # mock build_discord_embeds_from_supplement_request
    fake_embed = MagicMock()
    fake_embed.to_dict.return_value = {"embed": 1}
    monkeypatch.setattr(supplement_request, "build_discord_embeds_from_supplement_request", lambda d: [fake_embed])
    # mock send_webhook_message
    monkeypatch.setattr(supplement_request, "send_webhook_message", AsyncMock())
    resp = await supplement_request.receive_supplement_request(request)
    assert isinstance(resp, JSONResponse)
    assert resp.status_code == 200
    assert resp.body == b'{"status":"received"}'

@pytest.mark.asyncio
async def test_receive_supplement_request_webhook_error(monkeypatch):
    # 传入合法 agent_profile，确保能走到 send_webhook_message
    data = {
        "agent_profile": {
            "avatar_url": "url",
            "webhook_name": "wh",
            "channel_id": 1,
            "guild_id": 2,
            "capture_end": "discord",
            "agent_end": "missspec"
        }
    }
    request = MagicMock(spec=Request)
    request.json = AsyncMock(return_value=data)
    monkeypatch.setattr(supplement_request, "build_discord_embeds_from_supplement_request", lambda d: [])
    # send_webhook_message 抛异常
    monkeypatch.setattr(supplement_request, "send_webhook_message", AsyncMock(side_effect=Exception("fail")))
    with pytest.raises(Exception) as e:
        await supplement_request.receive_supplement_request(request)
    assert "fail" in str(e.value) 
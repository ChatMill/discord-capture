import pytest
from unittest.mock import AsyncMock, MagicMock
import sys

# 在 import capture 前 mock get_agent_base_url，避免 settings 校验
@pytest.fixture(autouse=True)
def patch_get_agent_base_url(monkeypatch):
    sys.modules["infrastructure.config.settings"] = MagicMock(get_agent_base_url=lambda svc: "http://agent/", AgentServiceName=MagicMock(MISS_SPEC="missspec"))
    yield

from domain.events.capture import Capture
from shared.agent_response import AgentResponse
import httpx

class AsyncClientContextManager:
    def __init__(self, client):
        self.client = client
    async def __aenter__(self):
        return self.client
    async def __aexit__(self, exc_type, exc, tb):
        pass

@pytest.mark.asyncio
async def test_notify_missspec_capture_success(monkeypatch):
    from interfaces.api.to_missspec import capture
    event = MagicMock(spec=Capture)
    event.dict.return_value = {"foo": "bar"}
    # mock httpx.AsyncClient
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "data": {"x": 1}}
    mock_client.post = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(capture.httpx, "AsyncClient", lambda *a, **kw: AsyncClientContextManager(mock_client))
    monkeypatch.setattr(capture, "AgentResponse", AgentResponse)
    resp = await capture.notify_missspec_capture(event)
    assert isinstance(resp, AgentResponse)
    assert resp.success is True
    assert resp.data == {"x": 1}

@pytest.mark.asyncio
async def test_notify_missspec_capture_http_error(monkeypatch):
    from interfaces.api.to_missspec import capture
    event = MagicMock(spec=Capture)
    event.dict.return_value = {"foo": "bar"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPError("fail")
    mock_client.post = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(capture.httpx, "AsyncClient", lambda *a, **kw: AsyncClientContextManager(mock_client))
    monkeypatch.setattr(capture, "AgentResponse", AgentResponse)
    with pytest.raises(httpx.HTTPError):
        await capture.notify_missspec_capture(event)

@pytest.mark.asyncio
async def test_notify_missspec_capture_timeout(monkeypatch):
    from interfaces.api.to_missspec import capture
    event = MagicMock(spec=Capture)
    event.dict.return_value = {"foo": "bar"}
    mock_client = MagicMock()
    mock_client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    monkeypatch.setattr(capture.httpx, "AsyncClient", lambda *a, **kw: AsyncClientContextManager(mock_client))
    monkeypatch.setattr(capture, "AgentResponse", AgentResponse)
    with pytest.raises(httpx.TimeoutException):
        await capture.notify_missspec_capture(event) 
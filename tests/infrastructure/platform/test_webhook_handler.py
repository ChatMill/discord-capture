import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import infrastructure.platform.webhook_handler as wh

class DummyTextChannel:
    def __init__(self, webhooks=None):
        self._webhooks = webhooks or []
    async def webhooks(self):
        return self._webhooks
    async def create_webhook(self, name):
        wh = MagicMock()
        wh.name = name
        wh.url = f"http://webhook/{name}"
        return wh

class DummyWebhook:
    def __init__(self, name, url):
        self.name = name
        self.url = url

class DummyAgentProfile:
    webhook_name = "wh"
    channel_id = 1
    avatar_url = "http://avatar"

@pytest.fixture(autouse=True)
def clear_webhook_cache():
    wh._webhook_cache.clear()
    yield
    wh._webhook_cache.clear()

@pytest.mark.asyncio
async def test_set_webhook_cached():
    wh._webhook_cache[("wh", 1)] = "http://cached"
    url = await wh.set_webhook("wh", 1, MagicMock())
    assert url == "http://cached"

@pytest.mark.asyncio
async def test_set_webhook_create(monkeypatch):
    bot_client = MagicMock()
    channel = DummyTextChannel()
    bot_client.fetch_channel = AsyncMock(return_value=channel)
    monkeypatch.setattr(wh.discord, "TextChannel", DummyTextChannel)
    url = await wh.set_webhook("wh", 1, bot_client)
    assert url.startswith("http://webhook/")
    assert ("wh", 1) in wh._webhook_cache

@pytest.mark.asyncio
async def test_set_webhook_existing(monkeypatch):
    bot_client = MagicMock()
    webhook = DummyWebhook("wh", "http://exists")
    channel = DummyTextChannel(webhooks=[webhook])
    bot_client.fetch_channel = AsyncMock(return_value=channel)
    monkeypatch.setattr(wh.discord, "TextChannel", DummyTextChannel)
    url = await wh.set_webhook("wh", 1, bot_client)
    assert url == "http://exists"
    assert ("wh", 1) in wh._webhook_cache

@pytest.mark.asyncio
async def test_set_webhook_not_text_channel(monkeypatch):
    bot_client = MagicMock()
    not_text_channel = MagicMock()
    monkeypatch.setattr(wh.discord, "TextChannel", DummyTextChannel)
    bot_client.fetch_channel = AsyncMock(return_value=not_text_channel)
    with pytest.raises(ValueError):
        await wh.set_webhook("wh", 1, bot_client)

@pytest.mark.asyncio
async def test_get_webhook_url_hit():
    wh._webhook_cache[("wh", 1)] = "http://cached"
    url = await wh.get_webhook_url("wh", 1)
    assert url == "http://cached"

@pytest.mark.asyncio
async def test_get_webhook_url_miss():
    url = await wh.get_webhook_url("wh", 2)
    assert url is None

@pytest.mark.asyncio
async def test_send_webhook_message_success(monkeypatch):
    wh._webhook_cache[("wh", 1)] = "http://cached"
    agent = DummyAgentProfile()
    mock_client = AsyncMock()
    mock_resp = MagicMock(status_code=200)
    mock_client.__aenter__.return_value = mock_client
    mock_client.post = AsyncMock(return_value=mock_resp)
    monkeypatch.setattr(wh.httpx, "AsyncClient", MagicMock(return_value=mock_client))
    await wh.send_webhook_message(agent, content="hi", embeds=[{"foo": "bar"}])
    mock_client.post.assert_awaited_once()

@pytest.mark.asyncio
async def test_send_webhook_message_no_url(monkeypatch):
    agent = DummyAgentProfile()
    monkeypatch.setattr(wh.httpx, "AsyncClient", MagicMock())
    # Should not raise, just skip sending
    await wh.send_webhook_message(agent, content="hi")

@pytest.mark.asyncio
async def test_send_webhook_message_httpx_error(monkeypatch):
    wh._webhook_cache[("wh", 1)] = "http://cached"
    agent = DummyAgentProfile()
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.post = AsyncMock(side_effect=Exception("fail"))
    monkeypatch.setattr(wh.httpx, "AsyncClient", MagicMock(return_value=mock_client))
    await wh.send_webhook_message(agent, content="hi") 
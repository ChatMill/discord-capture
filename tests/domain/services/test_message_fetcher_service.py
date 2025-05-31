import pytest
import asyncio
from domain.services.message_fetcher_service import MessageFetcherService
from domain.entities.message import Message

class DummyChannel:
    def __init__(self, messages):
        self._messages = messages
    async def fetch_message(self, mid):
        if mid in self._messages:
            return self._messages[mid]
        raise Exception("Not found")

class DummyDiscordClient:
    def __init__(self, messages):
        self._messages = messages
    def get_channel(self, channel_id):
        return DummyChannel(self._messages)
    async def fetch_channel(self, channel_id):
        return DummyChannel(self._messages)

class DummyMsg:
    def __init__(self, id, content, author_id, author_name, created_at):
        self.id = id
        self.content = content
        self.author = type("A", (), {"id": author_id, "display_name": author_name})()
        self.created_at = created_at

@pytest.mark.asyncio
async def test_fetch_messages_success():
    msg1 = DummyMsg(1, "hi", 10, "Alice", "2024-07-01T10:00:00Z")
    msg2 = DummyMsg(2, "yo", 20, "Bob", "2024-07-01T11:00:00Z")
    client = DummyDiscordClient({1: msg1, 2: msg2})
    service = MessageFetcherService(client)
    result = await service.fetch_messages(123, [1, 2])
    assert len(result) == 2
    assert result[0].content == "hi"
    assert result[1].author_name == "Bob"

@pytest.mark.asyncio
async def test_fetch_messages_with_missing():
    msg1 = DummyMsg(1, "hi", 10, "Alice", "2024-07-01T10:00:00Z")
    client = DummyDiscordClient({1: msg1})
    service = MessageFetcherService(client)
    result = await service.fetch_messages(123, [1, 2, 3])
    assert len(result) == 1
    assert result[0].id == "1" 
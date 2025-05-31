import pytest
import asyncio
from domain.repositories.message_repository import MessageRepository

class DummyMessageRepository(MessageRepository):
    def __init__(self):
        self._store = {}
    async def insert(self, message):
        if not isinstance(message, dict):
            raise ValueError("message must be dict")
        self._store[message.get("id")] = message
        return message.get("id")
    async def find(self, query):
        mid = query.get("id")
        return self._store.get(mid)

@pytest.mark.asyncio
async def test_message_repository_insert_and_find():
    repo = DummyMessageRepository()
    message = {"id": "m1", "foo": "bar"}
    mid = await repo.insert(message)
    assert mid == "m1"
    found = await repo.find({"id": "m1"})
    assert found == message

@pytest.mark.asyncio
async def test_message_repository_insert_invalid():
    repo = DummyMessageRepository()
    with pytest.raises(ValueError):
        await repo.insert([1, 2, 3])
    assert await repo.find({"id": "notfound"}) is None 
import pytest
import asyncio
from domain.repositories.payload_repository import PayloadRepository

class DummyPayloadRepository(PayloadRepository):
    def __init__(self):
        self._store = {}
    async def insert(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("payload must be dict")
        self._store[payload.get("id")] = payload
        return payload.get("id")
    async def find(self, query):
        pid = query.get("id")
        return self._store.get(pid)

@pytest.mark.asyncio
async def test_payload_repository_insert_and_find():
    repo = DummyPayloadRepository()
    payload = {"id": "p1", "foo": "bar"}
    pid = await repo.insert(payload)
    assert pid == "p1"
    found = await repo.find({"id": "p1"})
    assert found == payload

@pytest.mark.asyncio
async def test_payload_repository_insert_invalid():
    repo = DummyPayloadRepository()
    with pytest.raises(ValueError):
        await repo.insert([1, 2, 3])
    assert await repo.find({"id": "notfound"}) is None 
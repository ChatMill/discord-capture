import pytest
import asyncio
from domain.repositories.event_repository import EventRepository

class DummyEventRepository(EventRepository):
    def __init__(self):
        self._store = {}
    async def insert(self, event):
        if not isinstance(event, dict):
            raise ValueError("event must be dict")
        self._store[event.get("id")] = event
        return event.get("id")
    async def find(self, query):
        eid = query.get("id")
        return self._store.get(eid)

@pytest.mark.asyncio
async def test_event_repository_insert_and_find():
    repo = DummyEventRepository()
    event = {"id": "e1", "foo": "bar"}
    eid = await repo.insert(event)
    assert eid == "e1"
    found = await repo.find({"id": "e1"})
    assert found == event

@pytest.mark.asyncio
async def test_event_repository_insert_invalid():
    repo = DummyEventRepository()
    with pytest.raises(ValueError):
        await repo.insert([1, 2, 3])
    assert await repo.find({"id": "notfound"}) is None 
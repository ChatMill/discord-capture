import pytest
import asyncio
from domain.repositories.session_repository import SessionRepository

class DummySessionRepository(SessionRepository):
    def __init__(self):
        self._store = {}
    async def insert(self, session):
        if not isinstance(session, dict):
            raise ValueError("session must be dict")
        self._store[session.get("id")] = session
        return session.get("id")
    async def find(self, query):
        sid = query.get("id")
        return self._store.get(sid)

@pytest.mark.asyncio
async def test_session_repository_insert_and_find():
    repo = DummySessionRepository()
    session = {"id": "s1", "foo": "bar"}
    sid = await repo.insert(session)
    assert sid == "s1"
    found = await repo.find({"id": "s1"})
    assert found == session

@pytest.mark.asyncio
async def test_session_repository_insert_invalid():
    repo = DummySessionRepository()
    with pytest.raises(ValueError):
        await repo.insert([1, 2, 3])
    assert await repo.find({"id": "notfound"}) is None 
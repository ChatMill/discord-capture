import pytest
from unittest.mock import AsyncMock, MagicMock
from infrastructure.repositories.event_repository_impl import EventRepositoryImpl

class DummyEvent:
    event_id = "e1"
    payload_id = "p1"
    message_ids = ["m1", "m2"]
    agent_profile = {"foo": "bar"}

class DummyEventDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def dict(self):
        return self.__dict__
    event_id = "e1"
    payload_id = "p1"
    message_ids = ["m1", "m2"]
    agent_profile = {"foo": "bar"}

class DummyPayloadDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    payload_id = "p1"

class DummyPayload:
    pass

class DummyMessageDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    message_id = "m1"

class DummyMessage:
    pass

class DummyAgentProfile:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.__getitem__.side_effect = lambda name: {
        "events": MagicMock(),
        "payloads": MagicMock(),
        "messages": MagicMock()
    }[name]
    return db

def patch_convertors(monkeypatch):
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.EventConvertor.to_document", staticmethod(lambda e: DummyEventDoc(event_id=e.event_id, payload_id=e.payload_id, message_ids=e.message_ids, agent_profile=e.agent_profile)))
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.EventConvertor.to_entity", staticmethod(lambda doc, payload, messages, agent_profile: (doc, payload, messages, agent_profile)))
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.PayloadConvertor.to_entity", staticmethod(lambda doc, _: DummyPayload()))
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.MessageConvertor.to_entity", staticmethod(lambda doc: DummyMessage()))
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.EventDocument", DummyEventDoc)
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.PayloadDocument", DummyPayloadDoc)
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.MessageDocument", DummyMessageDoc)
    monkeypatch.setattr("infrastructure.repositories.event_repository_impl.AgentProfile", DummyAgentProfile)

@pytest.mark.asyncio
async def test_insert_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = EventRepositoryImpl(mock_db)
    repo.collection.update_one = AsyncMock(return_value=MagicMock(upserted_id=None))
    event = DummyEvent()
    result = await repo.insert(event)
    assert result == event.event_id
    repo.collection.update_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = EventRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"event_id": "e1", "payload_id": "p1", "message_ids": ["m1", "m2"], "agent_profile": {"foo": "bar"}})
    repo.payload_collection.find_one = AsyncMock(return_value={"payload_id": "p1"})
    repo.message_collection.find_one = AsyncMock(side_effect=[{"message_id": "m1"}, {"message_id": "m2"}])
    result = await repo.find({"event_id": "e1"})
    assert isinstance(result, tuple)  # (doc, payload, messages, agent_profile)
    repo.collection.find_one.assert_awaited_once()
    repo.payload_collection.find_one.assert_awaited_once()
    assert repo.message_collection.find_one.await_count == 2

@pytest.mark.asyncio
async def test_find_not_found(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = EventRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"event_id": "e1"})
    assert result is None

@pytest.mark.asyncio
async def test_find_payload_missing(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = EventRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"event_id": "e1", "payload_id": "p1", "message_ids": ["m1"], "agent_profile": {"foo": "bar"}})
    repo.payload_collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"event_id": "e1"})
    assert result is None

@pytest.mark.asyncio
async def test_find_message_missing(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = EventRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"event_id": "e1", "payload_id": "p1", "message_ids": ["m1", "m2"], "agent_profile": {"foo": "bar"}})
    repo.payload_collection.find_one = AsyncMock(return_value={"payload_id": "p1"})
    # m1 found, m2 missing
    repo.message_collection.find_one = AsyncMock(side_effect=[{"message_id": "m1"}, None])
    result = await repo.find({"event_id": "e1"})
    assert isinstance(result, tuple)
    assert len(result[2]) == 1  # only one message found 
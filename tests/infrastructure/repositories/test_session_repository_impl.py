import pytest
from unittest.mock import AsyncMock, MagicMock
from infrastructure.repositories.session_repository_impl import SessionRepositoryImpl

class DummySession:
    session_id = "s1"
    payload_id = "p1"
    source = {"foo": "bar"}

class DummySessionDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def dict(self):
        return self.__dict__
    session_id = "s1"
    payload_id = "p1"
    source = {"foo": "bar"}

class DummyPayloadDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    payload_id = "p1"

class DummyPayload:
    pass

class DummySource:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.__getitem__.side_effect = lambda name: {
        "sessions": MagicMock(),
        "payloads": MagicMock()
    }[name]
    return db

def patch_convertors(monkeypatch):
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.SessionConvertor.to_document", staticmethod(lambda s: DummySessionDoc(session_id=s.session_id, payload_id=s.payload_id, source=s.source)))
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.SessionConvertor.to_entity", staticmethod(lambda doc, source, payload: (doc, source, payload)))
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.PayloadConvertor.to_entity", staticmethod(lambda doc, _: DummyPayload()))
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.SessionDocument", DummySessionDoc)
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.PayloadDocument", DummyPayloadDoc)
    monkeypatch.setattr("infrastructure.repositories.session_repository_impl.Source", DummySource)

@pytest.mark.asyncio
async def test_insert_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = SessionRepositoryImpl(mock_db)
    repo.collection.update_one = AsyncMock(return_value=MagicMock(upserted_id=None))
    session = DummySession()
    result = await repo.insert(session)
    assert result == session.session_id
    repo.collection.update_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = SessionRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"session_id": "s1", "payload_id": "p1", "source": {"foo": "bar"}})
    repo.payload_collection.find_one = AsyncMock(return_value={"payload_id": "p1"})
    result = await repo.find({"session_id": "s1"})
    assert isinstance(result, tuple)  # (doc, source, payload)
    repo.collection.find_one.assert_awaited_once()
    repo.payload_collection.find_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_not_found(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = SessionRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"session_id": "s1"})
    assert result is None

@pytest.mark.asyncio
async def test_find_payload_missing(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = SessionRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"session_id": "s1", "payload_id": "p1", "source": {"foo": "bar"}})
    repo.payload_collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"session_id": "s1"})
    assert result is None 
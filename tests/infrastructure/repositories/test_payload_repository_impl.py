import pytest
from unittest.mock import AsyncMock, MagicMock
from infrastructure.repositories.payload_repository_impl import PayloadRepositoryImpl

class DummyPayload:
    payload_id = "p1"

class DummyPayloadDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def dict(self):
        return self.__dict__
    payload_id = "p1"

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.__getitem__.side_effect = lambda name: {"payloads": MagicMock()}[name]
    return db

def patch_convertors(monkeypatch):
    monkeypatch.setattr("infrastructure.repositories.payload_repository_impl.PayloadConvertor.to_document", staticmethod(lambda p: DummyPayloadDoc(payload_id=p.payload_id)))
    monkeypatch.setattr("infrastructure.repositories.payload_repository_impl.PayloadConvertor.to_entity", staticmethod(lambda doc, _: doc))
    monkeypatch.setattr("infrastructure.repositories.payload_repository_impl.PayloadDocument", DummyPayloadDoc)

@pytest.mark.asyncio
async def test_insert_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = PayloadRepositoryImpl(mock_db)
    repo.collection.update_one = AsyncMock(return_value=MagicMock(upserted_id=None))
    payload = DummyPayload()
    result = await repo.insert(payload)
    assert result == payload.payload_id
    repo.collection.update_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = PayloadRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"payload_id": "p1"})
    result = await repo.find({"payload_id": "p1"})
    assert isinstance(result, DummyPayloadDoc)
    repo.collection.find_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_not_found(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = PayloadRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"payload_id": "p1"})
    assert result is None 
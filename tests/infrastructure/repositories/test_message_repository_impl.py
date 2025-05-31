import pytest
from unittest.mock import AsyncMock, MagicMock
from infrastructure.repositories.message_repository_impl import MessageRepositoryImpl

class DummyMessage:
    message_id = "m1"

class DummyMessageDoc:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def dict(self):
        return self.__dict__
    message_id = "m1"

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.__getitem__.side_effect = lambda name: {"messages": MagicMock()}[name]
    return db

def patch_convertors(monkeypatch):
    monkeypatch.setattr("infrastructure.repositories.message_repository_impl.MessageConvertor.to_document", staticmethod(lambda m: DummyMessageDoc(message_id=m.message_id)))
    monkeypatch.setattr("infrastructure.repositories.message_repository_impl.MessageConvertor.to_entity", staticmethod(lambda doc: doc))
    monkeypatch.setattr("infrastructure.repositories.message_repository_impl.MessageDocument", DummyMessageDoc)

@pytest.mark.asyncio
async def test_insert_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = MessageRepositoryImpl(mock_db)
    repo.collection.update_one = AsyncMock(return_value=MagicMock(upserted_id=None))
    message = DummyMessage()
    result = await repo.insert(message)
    assert result == message.message_id
    repo.collection.update_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_success(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = MessageRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value={"message_id": "m1"})
    result = await repo.find({"message_id": "m1"})
    assert isinstance(result, DummyMessageDoc)
    repo.collection.find_one.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_not_found(mock_db, monkeypatch):
    patch_convertors(monkeypatch)
    repo = MessageRepositoryImpl(mock_db)
    repo.collection.find_one = AsyncMock(return_value=None)
    result = await repo.find({"message_id": "m1"})
    assert result is None 
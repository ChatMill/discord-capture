import sys
import types
from unittest.mock import MagicMock, AsyncMock
import pytest
import importlib

# 彻底mock掉 capture_handler.py 的所有外部依赖模块
mock_handle_capture_command = AsyncMock()
mock_MessageFetcherService = MagicMock()
mock_CaptureMessageValidator = MagicMock()
mock_build_source = MagicMock()
mock_build_spec_payload = MagicMock()
mock_build_capture_event = MagicMock()
mock_build_session = MagicMock()
mock_session_repo = MagicMock()
mock_payload_repo = MagicMock()
mock_event_repo = MagicMock()
mock_message_repo = MagicMock()
mock_AsyncIOMotorClient = MagicMock()

sys.modules['application.services.missspec.capture'] = types.SimpleNamespace(
    handle_capture_command=mock_handle_capture_command
)
sys.modules['domain.services.message_fetcher_service'] = types.SimpleNamespace(
    MessageFetcherService=mock_MessageFetcherService
)
sys.modules['domain.services.capture_message_validator'] = types.SimpleNamespace(
    CaptureMessageValidator=mock_CaptureMessageValidator
)
sys.modules['interfaces.schemas.source_schema'] = types.SimpleNamespace(
    build_source=mock_build_source
)
sys.modules['interfaces.schemas.payload_schema'] = types.SimpleNamespace(
    build_spec_payload=mock_build_spec_payload
)
sys.modules['interfaces.schemas.event_schema'] = types.SimpleNamespace(
    build_capture_event=mock_build_capture_event
)
sys.modules['interfaces.schemas.session_schema'] = types.SimpleNamespace(
    build_session=mock_build_session
)
sys.modules['infrastructure.repositories.session_repository_impl'] = types.SimpleNamespace(
    SessionRepositoryImpl=MagicMock()
)
sys.modules['infrastructure.repositories.payload_repository_impl'] = types.SimpleNamespace(
    PayloadRepositoryImpl=MagicMock()
)
sys.modules['infrastructure.repositories.event_repository_impl'] = types.SimpleNamespace(
    EventRepositoryImpl=MagicMock()
)
sys.modules['infrastructure.repositories.message_repository_impl'] = types.SimpleNamespace(
    MessageRepositoryImpl=MagicMock()
)
sys.modules['motor.motor_asyncio'] = types.SimpleNamespace(
    AsyncIOMotorClient=mock_AsyncIOMotorClient
)

import application.handlers.missspec.capture_handler as handler

# patch handler作用域下的repo为AsyncMock，避免await报错
def patch_handler_repos():
    handler.session_repo = MagicMock()
    handler.session_repo.insert = AsyncMock()
    handler.payload_repo = MagicMock()
    handler.payload_repo.insert = AsyncMock()
    handler.event_repo = MagicMock()
    handler.event_repo.insert = AsyncMock()
    handler.message_repo = MagicMock()
    handler.message_repo.insert = AsyncMock()
    # 修正 fetcher mock：所有 fetch_messages 都用 AsyncMock
    fetcher = MagicMock()
    fetcher.fetch_messages = AsyncMock(return_value=[])
    handler.fetcher = fetcher

patch_handler_repos()

class DummyUser:
    def __init__(self, id=123, display_name="tester"):
        self.id = id
        self.display_name = display_name

class DummyInteraction:
    def __init__(self, channel_id=1, guild_id=2, id=3, user=None, client=None):
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.id = id
        self.user = user or DummyUser()
        self.client = client or MagicMock()

@pytest.mark.asyncio
async def test_capture_handler_main_flow():
    interaction = DummyInteraction()
    message_ids = "1,2,3"
    participants = "alice, bob"
    fetched_messages = [MagicMock(id=str(i)) for i in [1,2,3]]
    not_found_str_ids = []
    deduped_ids = ["1","2","3"]

    # 修正：mock fetcher 实例的 fetch_messages 为 AsyncMock
    mock_fetcher_instance = MagicMock()
    mock_fetcher_instance.fetch_messages = AsyncMock(return_value=fetched_messages)
    mock_MessageFetcherService.return_value = mock_fetcher_instance

    mock_CaptureMessageValidator.fetch_and_validate = AsyncMock(return_value=(fetched_messages, not_found_str_ids))
    mock_CaptureMessageValidator.deduplicate_message_ids = MagicMock(return_value=deduped_ids)
    mock_CaptureMessageValidator.format_not_found_message = MagicMock(return_value="")
    mock_session_repo.insert = AsyncMock()
    mock_payload_repo.insert = AsyncMock()
    mock_event_repo.insert = AsyncMock()
    mock_message_repo.insert = AsyncMock()
    reply = await handler.capture_handler(interaction, message_ids, participants)
    assert "Message IDs: [1, 2, 3]" in reply
    assert "Participants: ['alice', 'bob']" in reply
    mock_handle_capture_command.assert_called_once()

@pytest.mark.asyncio
async def test_capture_handler_not_found_ids():
    interaction = DummyInteraction()
    message_ids = "1,2,3"
    participants = None
    fetched_messages = [MagicMock(id="1")]
    not_found_str_ids = ["2","3"]
    deduped_ids = ["1","2","3"]
    not_found_msg = "Sorry, I couldn't find these message(s): 2, 3.\n"

    # 修正：mock fetcher 实例的 fetch_messages 为 AsyncMock
    mock_fetcher_instance = MagicMock()
    mock_fetcher_instance.fetch_messages = AsyncMock(return_value=fetched_messages)
    mock_MessageFetcherService.return_value = mock_fetcher_instance

    mock_CaptureMessageValidator.fetch_and_validate = AsyncMock(return_value=(fetched_messages, not_found_str_ids))
    mock_CaptureMessageValidator.deduplicate_message_ids = MagicMock(return_value=deduped_ids)
    mock_CaptureMessageValidator.format_not_found_message = MagicMock(return_value=not_found_msg)
    mock_session_repo.insert = AsyncMock()
    mock_payload_repo.insert = AsyncMock()
    mock_event_repo.insert = AsyncMock()
    mock_message_repo.insert = AsyncMock()
    reply = await handler.capture_handler(interaction, message_ids, participants)
    assert not_found_msg in reply
    assert "Participants: None" in reply

# 恢复被 mock 的模块，避免污染其它测试
for mod in [
    'application.services.missspec.capture',
    'domain.services.message_fetcher_service',
    'domain.services.capture_message_validator',
    'interfaces.schemas.source_schema',
    'interfaces.schemas.payload_schema',
    'interfaces.schemas.event_schema',
    'interfaces.schemas.session_schema',
    'infrastructure.repositories.session_repository_impl',
    'infrastructure.repositories.payload_repository_impl',
    'infrastructure.repositories.event_repository_impl',
    'infrastructure.repositories.message_repository_impl',
    'motor.motor_asyncio',
]:
    sys.modules.pop(mod, None)
    try:
        importlib.reload(importlib.import_module(mod))
    except Exception:
        pass  # 有些模块可能本轮测试没用到，忽略 
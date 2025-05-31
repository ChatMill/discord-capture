import sys
import types
from unittest.mock import MagicMock, AsyncMock

import pytest
import importlib

# 在import capture前，彻底mock掉其所有外部依赖模块，防止递归import settings
mock_notify = MagicMock()
mock_get_webhook_url = AsyncMock()
mock_set_webhook = AsyncMock()
mock_send_webhook_message = AsyncMock()
mock_agent_response_with_retry = AsyncMock()

sys.modules['interfaces.api.to_missspec.capture'] = types.SimpleNamespace(
    notify_missspec_capture=mock_notify
)
sys.modules['infrastructure.platform.webhook_handler'] = types.SimpleNamespace(
    get_webhook_url=mock_get_webhook_url,
    set_webhook=mock_set_webhook,
    send_webhook_message=mock_send_webhook_message
)
sys.modules['application.services.feedback_utils'] = types.SimpleNamespace(
    agent_response_with_retry=mock_agent_response_with_retry
)

from application.services.missspec import capture

class DummyInteraction:
    class DummyClient:
        pass
    client = DummyClient()

class DummyEvent:
    class DummyAgentProfile:
        webhook_name = "wh"
        channel_id = 1
    agent_profile = DummyAgentProfile()

def make_event():
    return DummyEvent()

def make_interaction():
    return DummyInteraction()

@pytest.mark.asyncio
async def test_handle_capture_command_webhook_exists():
    mock_get_webhook_url.return_value = "url"
    await capture.handle_capture_command(make_interaction(), make_event())
    mock_agent_response_with_retry.assert_awaited_once()
    mock_set_webhook.assert_not_awaited()
    mock_send_webhook_message.assert_not_awaited()
    mock_agent_response_with_retry.reset_mock()
    mock_set_webhook.reset_mock()
    mock_send_webhook_message.reset_mock()

@pytest.mark.asyncio
async def test_handle_capture_command_webhook_needs_set():
    mock_get_webhook_url.return_value = None
    await capture.handle_capture_command(make_interaction(), make_event())
    mock_set_webhook.assert_awaited_once()
    mock_agent_response_with_retry.assert_awaited_once()
    mock_send_webhook_message.assert_not_awaited()
    mock_agent_response_with_retry.reset_mock()
    mock_set_webhook.reset_mock()
    mock_send_webhook_message.reset_mock()

@pytest.mark.asyncio
async def test_handle_capture_command_agent_response_error():
    mock_get_webhook_url.return_value = "url"
    mock_agent_response_with_retry.side_effect = Exception("fail")
    with pytest.raises(Exception):
        await capture.handle_capture_command(make_interaction(), make_event())
    mock_agent_response_with_retry.side_effect = None
    mock_agent_response_with_retry.reset_mock()

# 恢复被 mock 的模块，避免污染其它测试
for mod in [
    'interfaces.api.to_missspec.capture',
    'infrastructure.platform.webhook_handler',
    'application.services.feedback_utils',
]:
    sys.modules.pop(mod, None)
    try:
        importlib.reload(importlib.import_module(mod))
    except Exception:
        pass  # 有些模块可能本轮测试没用到，忽略

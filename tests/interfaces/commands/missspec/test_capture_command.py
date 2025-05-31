import pytest
from interfaces.commands.missspec import capture
from unittest.mock import AsyncMock, MagicMock

class DummyInteraction:
    def __init__(self):
        self.response = MagicMock()
        self.response.send_message = AsyncMock()

def test_parse_message_ids_normal():
    s = "123, 456,789"
    result = capture.parse_message_ids(s)
    assert result == [123, 456, 789]

def test_parse_message_ids_empty():
    assert capture.parse_message_ids("") == []

def test_parse_message_ids_invalid():
    # 按实现，遇到异常直接返回 []
    assert capture.parse_message_ids("abc,1,2") == []

def test_register_capture_command_calls_handler(monkeypatch):
    """
    Test that the capture_command registers the command handler.
    """
    fake_tree = MagicMock()
    monkeypatch.setattr(capture, "capture_handler", AsyncMock(return_value="reply"))
    capture.register_capture_command(fake_tree)
    assert fake_tree.command.called 
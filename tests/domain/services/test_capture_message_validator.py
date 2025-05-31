import pytest
import asyncio
from domain.services.capture_message_validator import CaptureMessageValidator
from domain.entities.message import Message

class DummyFetcher:
    async def fetch_messages(self, channel_id, message_ids):
        # Simulate: only return Message for ids that are digits
        return [Message(id=mid, author_id="a", author_name="n", content="c", timestamp="t")
                for mid in message_ids if mid.isdigit()]

class TestCaptureMessageValidator:
    """
    Unit tests for CaptureMessageValidator utility class.
    """
    def test_deduplicate_message_ids(self):
        ids = ["1", "2", "1", "3", "2"]
        deduped = CaptureMessageValidator.deduplicate_message_ids(ids)
        assert deduped == ["1", "2", "3"]

    @pytest.mark.asyncio
    async def test_fetch_and_validate(self):
        fetcher = DummyFetcher()
        message_ids = ["1", "x", "2", "y"]
        found, not_found = await CaptureMessageValidator.fetch_and_validate(message_ids, fetcher, "chan1")
        found_ids = [m.id for m in found]
        assert set(found_ids) == {"1", "2"}
        assert set(not_found) == {"x", "y"}

    def test_format_not_found_message(self):
        msg = CaptureMessageValidator.format_not_found_message(["a", "b"])
        assert "a, b" in msg
        assert "couldn't find" in msg
        assert CaptureMessageValidator.format_not_found_message([]) == "" 
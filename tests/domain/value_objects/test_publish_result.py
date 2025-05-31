import pytest
from domain.value_objects.publish_result import PublishResult

class TestPublishResult:
    """
    Unit tests for the PublishResult value object.
    """
    def test_publish_result_creation(self):
        result = PublishResult(status="success", platform="discord", url="http://x", message="ok", id="123")
        assert result.status == "success"
        assert result.platform == "discord"
        assert result.url == "http://x"
        assert result.message == "ok"
        assert result.id == "123"

    def test_publish_result_optional_fields(self):
        result = PublishResult(status="fail", platform="discord")
        assert result.status == "fail"
        assert result.url is None
        assert result.message is None
        assert result.id is None

    def test_publish_result_serialization(self):
        data = {"status": "s", "platform": "p", "url": "u", "message": "m", "id": "i"}
        result = PublishResult(**data)
        assert result.dict() == data
        result2 = PublishResult.parse_obj(result.dict())
        assert result2 == result 
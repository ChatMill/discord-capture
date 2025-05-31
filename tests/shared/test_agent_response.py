import pytest
from shared.agent_response import AgentResponse

class TestAgentResponse:
    """
    Unit tests for the AgentResponse Pydantic model.
    """
    def test_success_response(self):
        """Test creating a successful AgentResponse."""
        resp = AgentResponse(success=True, error=None, data={"foo": "bar"})
        assert resp.success is True
        assert resp.error is None
        assert resp.data == {"foo": "bar"}

    def test_error_response(self):
        """Test creating an error AgentResponse."""
        resp = AgentResponse(success=False, error="Some error", data=None)
        assert resp.success is False
        assert resp.error == "Some error"
        assert resp.data is None

    def test_serialization_and_deserialization(self):
        """Test serialization and deserialization of AgentResponse."""
        resp = AgentResponse(success=True, error=None, data={"x": 1})
        data = resp.dict()
        resp2 = AgentResponse.parse_obj(data)
        assert resp2 == resp

    def test_missing_optional_fields(self):
        """Test that missing optional fields default to None."""
        resp = AgentResponse(success=True)
        assert resp.error is None
        assert resp.data is None 
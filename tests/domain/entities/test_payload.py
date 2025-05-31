import pytest
from domain.entities.payload import Payload

class TestPayload:
    """
    Unit tests for the Payload base entity.
    """
    def test_payload_creation(self):
        """Test creating a Payload entity with all fields."""
        payload = Payload(chatmill_id="cmid", external_id="eid", message_ids=["m1", "m2"])
        assert payload.chatmill_id == "cmid"
        assert payload.external_id == "eid"
        assert payload.message_ids == ["m1", "m2"]

    def test_payload_optional_external_id(self):
        """Test Payload entity with optional external_id missing."""
        payload = Payload(chatmill_id="cmid2", message_ids=["m3"])
        assert payload.chatmill_id == "cmid2"
        assert payload.external_id is None
        assert payload.message_ids == ["m3"]

    def test_payload_serialization(self):
        """Test serialization and deserialization of Payload entity."""
        data = {"chatmill_id": "c1", "external_id": "e1", "message_ids": ["x"]}
        payload = Payload(**data)
        assert payload.dict() == data
        payload2 = Payload.parse_obj(payload.dict())
        assert payload2 == payload

    def test_payload_missing_required(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(Exception):
            Payload(external_id="eid", message_ids=["m1"])  # missing chatmill_id 
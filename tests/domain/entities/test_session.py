import pytest
from domain.entities.session import Session
from domain.value_objects.source import Source
from domain.entities.payload import Payload

class TestSession:
    """
    Unit tests for the Session domain entity.
    """
    def test_session_creation(self):
        """Test creating a Session entity with all fields."""
        source = Source(
            platform="discord",
            organization_id="org1",
            project_id="proj1",
            message_ids=[1, 2, 3],
            participants=["u1", "u2"]
        )
        payload = Payload(chatmill_id="cmid", external_id="eid", message_ids=["m1", "m2"])
        session = Session(
            session_id="s1",
            source=source,
            history=["e1", "e2"],
            agent="missspec",
            payload=payload
        )
        assert session.session_id == "s1"
        assert session.source == source
        assert session.history == ["e1", "e2"]
        assert session.agent == "missspec"
        assert session.payload == payload

    def test_session_serialization(self):
        """Test serialization and deserialization of Session entity."""
        source = Source(
            platform="discord",
            organization_id="org2",
            project_id="proj2",
            message_ids=[4, 5],
            participants=["u3"]
        )
        payload = Payload(chatmill_id="cmid2", external_id=None, message_ids=["m3"])
        data = {
            "session_id": "s2",
            "source": source.dict(),
            "history": ["e3"],
            "agent": "agent2",
            "payload": payload.dict()
        }
        session = Session.parse_obj(data)
        assert session.session_id == "s2"
        assert session.source.platform == "discord"
        assert session.payload.chatmill_id == "cmid2"
        assert session.history == ["e3"]
        assert session.agent == "agent2"
        # round-trip
        session2 = Session.parse_obj(session.dict())
        assert session2 == session

    def test_session_missing_fields(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(Exception):
            Session(session_id="s3", source=None, history=[], agent="a", payload=None) 
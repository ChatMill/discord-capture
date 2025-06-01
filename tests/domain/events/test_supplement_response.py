import pytest
from domain.events.supplement_response import SupplementResponse, EventType
from domain.entities.spec import Spec
from domain.entities.message import Message

class TestSupplementResponseEvent:
    """
    Unit tests for the SupplementResponse event entity.
    """
    def test_supplement_response_creation(self):
        spec = Spec(chatmill_id="cmid", title="T", description="D", message_ids=["m1"])
        msg = Message(id="1", author_id="a", author_name="n", content="c", timestamp="t")
        event = SupplementResponse(
            session_id="s1",
            event_id="e1",
            operator_id="u1",
            payload=spec,
            history=["e0"],
            supplement_messages=["extra info"],
            messages=[msg]
        )
        assert event.session_id == "s1"
        assert event.payload == spec
        assert event.supplement_messages == ["extra info"]
        assert event.messages == [msg]
        assert event.event_type == EventType.SUPPLEMENT_RESPONSE

    def test_supplement_response_serialization(self):
        spec = Spec(chatmill_id="cmid2", title="T2", description="D2", message_ids=["m2"])
        msg = Message(id="2", author_id="b", author_name="m", content="d", timestamp="t2")
        data = {
            "session_id": "s2",
            "event_id": "e2",
            "operator_id": "u2",
            "payload": spec.dict(),
            "history": ["e1"],
            "supplement_messages": ["info"],
            "messages": [msg.dict()],
            "event_type": "supplement_response"
        }
        event = SupplementResponse.parse_obj(data)
        assert event.session_id == "s2"
        assert event.payload.title == "T2"
        assert event.supplement_messages == ["info"]
        assert event.messages[0].id == "2"
        # round-trip
        event2 = SupplementResponse.parse_obj(event.dict())
        assert event2 == event

    def test_supplement_response_missing_required(self):
        with pytest.raises(Exception):
            SupplementResponse(session_id="s", event_id="e", operator_id="u", payload=None, history=None, supplement_messages=None, messages=None) 
import pytest
from domain.events.base_event import Event, EventType
from domain.entities.payload import Payload

class TestEvent:
    """
    Unit tests for the Event base class and EventType enum.
    """
    def test_event_type_enum(self):
        assert EventType.CAPTURE == "capture"
        assert EventType.SUPPLEMENT_REQUEST == "supplement_request"
        assert EventType.PUBLISH_RESULT == "publish_result"

    def test_event_creation(self):
        payload = Payload(chatmill_id="c1", external_id="e1", message_ids=["m1"])
        event = Event(
            event_type=EventType.CAPTURE,
            session_id="s1",
            event_id="e1",
            operator_id="u1",
            payload=payload,
            history=["e0"]
        )
        assert event.event_type == EventType.CAPTURE
        assert event.session_id == "s1"
        assert event.payload == payload
        assert event.history == ["e0"]

    def test_event_serialization(self):
        payload = Payload(chatmill_id="c2", external_id=None, message_ids=["m2"])
        data = {
            "event_type": "capture",
            "session_id": "s2",
            "event_id": "e2",
            "operator_id": "u2",
            "payload": payload.dict(),
            "history": ["e1"]
        }
        event = Event.parse_obj(data)
        assert event.event_type == EventType.CAPTURE
        assert event.session_id == "s2"
        assert event.payload.chatmill_id == "c2"
        # round-trip
        event2 = Event.parse_obj(event.dict())
        assert event2 == event

    def test_event_missing_required(self):
        with pytest.raises(Exception):
            Event(event_type=EventType.CAPTURE, session_id="s", event_id="e", operator_id="u", payload=None, history=None) 
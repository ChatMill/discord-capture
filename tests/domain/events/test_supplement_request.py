import pytest
from domain.events.supplement_request import SupplementRequest, EventType
from domain.entities.task import Task

class TestSupplementRequestEvent:
    """
    Unit tests for the SupplementRequest event entity.
    """
    def test_supplement_request_creation(self):
        task = Task(chatmill_id="cmid", title="T", description="D", message_ids=["m1"])
        event = SupplementRequest(
            session_id="s1",
            event_id="e1",
            operator_id="u1",
            payload=task,
            history=["e0"],
            question="What is your requirement?"
        )
        assert event.session_id == "s1"
        assert event.payload == task
        assert event.question == "What is your requirement?"
        assert event.event_type == EventType.SUPPLEMENT_REQUEST

    def test_supplement_request_serialization(self):
        task = Task(chatmill_id="cmid2", title="T2", description="D2", message_ids=["m2"])
        data = {
            "session_id": "s2",
            "event_id": "e2",
            "operator_id": "u2",
            "payload": task.dict(),
            "history": ["e1"],
            "question": "Q?",
            "event_type": "supplement_request"
        }
        event = SupplementRequest.parse_obj(data)
        assert event.session_id == "s2"
        assert event.payload.title == "T2"
        assert event.question == "Q?"
        # round-trip
        event2 = SupplementRequest.parse_obj(event.dict())
        assert event2 == event

    def test_supplement_request_missing_required(self):
        with pytest.raises(Exception):
            SupplementRequest(session_id="s", event_id="e", operator_id="u", payload=None, history=None, question=None) 
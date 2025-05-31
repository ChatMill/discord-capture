import pytest
from domain.events.capture import Capture, EventType
from domain.entities.message import Message
from domain.entities.task import Task
from domain.value_objects.agent_profile import AgentProfile

class TestCaptureEvent:
    """
    Unit tests for the Capture event entity.
    """
    def test_capture_event_creation(self):
        task = Task(chatmill_id="cmid", title="T", description="D", message_ids=["m1"])
        msg = Message(id="1", author_id="a", author_name="n", content="c", timestamp="t")
        agent_profile = AgentProfile(webhook_name="wh", channel_id=1, guild_id=2)
        event = Capture(
            session_id="s1",
            event_id="e1",
            operator_id="u1",
            payload=task,
            history=["e0"],
            messages=[msg],
            agent_profile=agent_profile
        )
        assert event.session_id == "s1"
        assert event.payload == task
        assert event.messages == [msg]
        assert event.agent_profile == agent_profile
        assert event.event_type == EventType.CAPTURE

    def test_capture_event_serialization(self):
        task = Task(chatmill_id="cmid2", title="T2", description="D2", message_ids=["m2"])
        msg = Message(id="2", author_id="b", author_name="m", content="d", timestamp="t2")
        agent_profile = AgentProfile(webhook_name="wh2", channel_id=3, guild_id=4)
        data = {
            "session_id": "s2",
            "event_id": "e2",
            "operator_id": "u2",
            "payload": task.dict(),
            "history": ["e1"],
            "messages": [msg.dict()],
            "agent_profile": agent_profile.dict(),
            "event_type": "capture"
        }
        event = Capture.parse_obj(data)
        assert event.session_id == "s2"
        assert event.payload.title == "T2"
        assert event.messages[0].id == "2"
        assert event.agent_profile.webhook_name == "wh2"
        # round-trip
        event2 = Capture.parse_obj(event.dict())
        assert event2 == event

    def test_capture_event_missing_required(self):
        with pytest.raises(Exception):
            Capture(session_id="s", event_id="e", operator_id="u", payload=None, history=None, messages=None, agent_profile=None) 
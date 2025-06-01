from infrastructure.convertors.event_convertor import EventConvertor
from domain.events.capture import Capture
from infrastructure.persistence.event_document import EventDocument
from domain.entities.spec import Spec
from domain.entities.message import Message
from domain.value_objects.agent_profile import AgentProfile
from domain.events.base_event import EventType

import pytest

def build_agent_profile():
    return AgentProfile(
        avatar_url="http://avatar.url",
        webhook_name="webhook1",
        channel_id=123,
        guild_id=456,
        capture_end="discord",
        agent_end="missspec"
    )

def build_message(mid):
    return Message(
        id=mid,
        author_id="aid",
        author_name="aname",
        content="msg content",
        timestamp="2024-01-01T12:00:00Z"
    )

def build_spec(pid):
    return Spec(
        chatmill_id=pid,
        external_id="eid",
        message_ids=["m1", "m2"],
        title="title",
        description="desc",
        start_time="2024-01-01T00:00:00Z",
        end_time="2024-01-02T00:00:00Z",
        storypoints=3.5,
        assignees=["user1"],
        priority="high",
        parent_spec=None,
        sub_specs=[]
    )

def test_to_document_id():
    payload = build_spec("pid")
    messages = [build_message("m1"), build_message("m2")]
    agent_profile = build_agent_profile()
    event = Capture(
        event_id="eid",
        session_id="sid",
        operator_id="oid",
        payload=payload,
        messages=messages,
        agent_profile=agent_profile,
        history=["h1", "h2"],
        event_type=EventType.CAPTURE
    )
    doc = EventConvertor.to_document(event)
    assert doc.event_id == "eid"
    assert doc.payload_id == payload.chatmill_id
    assert doc.message_ids == ["m1", "m2"]
    assert doc.agent_profile == agent_profile.dict()
    assert doc.event_type == "capture"

def test_to_document_agent_profile_dict():
    payload = build_spec("pid")
    agent_profile = build_agent_profile()
    event = Capture(
        event_id="eid",
        session_id="sid",
        operator_id="oid",
        payload=payload,
        messages=[],
        agent_profile=agent_profile,
        history=[],
        event_type=EventType.CAPTURE
    )
    doc = EventConvertor.to_document(event)
    assert doc.agent_profile == agent_profile.dict()

def test_to_document_event_type_value():
    payload = build_spec("pid")
    agent_profile = build_agent_profile()
    event = Capture(
        event_id="eid",
        session_id="sid",
        operator_id="oid",
        payload=payload,
        messages=[],
        agent_profile=agent_profile,
        history=[],
        event_type=EventType.CAPTURE
    )
    doc = EventConvertor.to_document(event)
    assert doc.event_type == "capture"

def test_to_entity():
    doc = EventDocument(
        event_id="eid",
        session_id="sid",
        operator_id="oid",
        payload_id="pid",
        message_ids=["m1", "m2"],
        agent_profile=build_agent_profile().dict(),
        event_type="capture",
        agent="missspec"
    )
    payload = build_spec("pid")
    messages = [build_message("m1"), build_message("m2")]
    agent_profile = build_agent_profile()
    entity = EventConvertor.to_entity(doc, payload, messages, agent_profile)
    assert entity.event_id == "eid"
    assert entity.session_id == "sid"
    assert entity.payload == payload
    assert entity.messages == messages
    assert entity.agent_profile == agent_profile
    assert entity.history == []
    assert entity.event_type == "capture" 
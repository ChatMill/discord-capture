import pytest
from interfaces.schemas import session_schema
from domain.value_objects.source import Source
from domain.entities.payload import Payload
from domain.events.base_event import Event
from domain.entities.spec import Spec

class DummyEvent(Event):
    event_id: str
    session_id: str
    operator_id: str
    payload: Payload
    history: list

    def __init__(self, event_id):
        super().__init__(event_type="capture", session_id="sid", event_id=event_id, operator_id="op", payload=Spec(chatmill_id="cmid", message_ids=["m1"], title="t", description="d"), history=[])


def test_build_session():
    # 用真实 Source、Payload、Event
    source = Source(platform="discord", organization_id="org1", project_id="proj1", message_ids=[1], participants=["u1"])
    spec = Spec(chatmill_id="cmid", message_ids=["m1"], title="t", description="d")
    event = DummyEvent(event_id="eid")
    session_id = "sid"
    session = session_schema.build_session(source, spec, event, session_id)
    # 检查 Session 字段
    assert session.session_id == session_id
    assert session.source == source
    assert session.payload == spec
    assert session.history == ["eid"]
    assert session.agent == "missspec" 
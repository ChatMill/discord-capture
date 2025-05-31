import pytest
from infrastructure.convertors.session_convertor import SessionConvertor
from domain.entities.session import Session
from infrastructure.persistence.session_document import SessionDocument
from domain.entities.payload import Payload
from domain.value_objects.source import Source

def test_to_document():
    source = Source(
        platform="discord",
        organization_id="org1",
        project_id="proj1",
        message_ids=[1, 2, 3],
        participants=["user1", "user2"]
    )
    payload = Payload(
        chatmill_id="cmid",
        external_id=None,
        message_ids=["m1", "m2"]
    )
    session = Session(
        session_id="sid",
        source=source,
        payload=payload,
        history=["e1", "e2"],
        agent="agent1"
    )
    doc = SessionConvertor.to_document(session)
    assert doc.session_id == "sid"
    assert doc.source == source.dict()
    assert doc.payload_id == payload.chatmill_id
    assert doc.history == ["e1", "e2"]
    assert doc.agent == "agent1"

def test_to_document_source_dict():
    # source is already a dict
    source_dict = {
        "platform": "discord",
        "organization_id": "org1",
        "project_id": "proj1",
        "message_ids": [1, 2, 3],
        "participants": ["user1", "user2"]
    }
    payload = Payload(chatmill_id="cmid", message_ids=["m1"])  # external_id=None
    session = Session(
        session_id="sid",
        source=Source(**source_dict),
        payload=payload,
        history=[],
        agent="agent1"
    )
    # 直接传 dict
    session_dict_source = session.copy(update={"source": source_dict})
    doc = SessionConvertor.to_document(session_dict_source)
    assert doc.source == source_dict

def test_to_entity():
    doc = SessionDocument(
        session_id="sid",
        source={
            "platform": "discord",
            "organization_id": "org1",
            "project_id": "proj1",
            "message_ids": [1, 2, 3],
            "participants": ["user1", "user2"]
        },
        payload_id="cmid",
        history=["e1", "e2"],
        agent="agent1"
    )
    source = Source(
        platform="discord",
        organization_id="org1",
        project_id="proj1",
        message_ids=[1, 2, 3],
        participants=["user1", "user2"]
    )
    payload = Payload(chatmill_id="cmid", message_ids=["m1"])  # external_id=None
    session = SessionConvertor.to_entity(doc, source, payload)
    assert session.session_id == "sid"
    assert session.source == source
    assert session.payload == payload
    assert session.history == ["e1", "e2"]
    assert session.agent == "agent1" 
from infrastructure.convertors.message_convertor import MessageConvertor
from domain.entities.message import Message
from infrastructure.persistence.message_document import MessageDocument

def test_to_document():
    msg = Message(
        id="mid",
        author_id="aid",
        author_name="aname",
        content="hello",
        timestamp="2024-01-01T12:00:00Z"
    )
    doc = MessageConvertor.to_document(msg)
    assert doc.message_id == "mid"
    assert doc.author_id == "aid"
    assert doc.author_name == "aname"
    assert doc.content == "hello"
    assert doc.timestamp == "2024-01-01T12:00:00Z"

def test_to_entity():
    doc = MessageDocument(
        message_id="mid",
        author_id="aid",
        author_name="aname",
        content="hello",
        timestamp="2024-01-01T12:00:00Z"
    )
    msg = MessageConvertor.to_entity(doc)
    assert msg.id == "mid"
    assert msg.author_id == "aid"
    assert msg.author_name == "aname"
    assert msg.content == "hello"
    assert msg.timestamp == "2024-01-01T12:00:00Z" 
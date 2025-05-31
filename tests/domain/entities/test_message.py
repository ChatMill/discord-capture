import pytest
from domain.entities.message import Message

class TestMessage:
    """
    Unit tests for the Message domain entity.
    """
    def test_message_creation(self):
        """Test creating a Message entity with all fields."""
        msg = Message(
            id="123",
            author_id="u1",
            author_name="Alice",
            content="Hello world!",
            timestamp="2024-07-01T12:00:00Z"
        )
        assert msg.id == "123"
        assert msg.author_id == "u1"
        assert msg.author_name == "Alice"
        assert msg.content == "Hello world!"
        assert msg.timestamp == "2024-07-01T12:00:00Z"

    def test_message_serialization(self):
        """Test serialization and deserialization of Message entity."""
        data = {
            "id": "456",
            "author_id": "u2",
            "author_name": "Bob",
            "content": "Test content",
            "timestamp": "2024-07-01T13:00:00Z"
        }
        msg = Message(**data)
        assert msg.dict() == data
        msg2 = Message.parse_obj(msg.dict())
        assert msg2 == msg

    def test_message_missing_fields(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(Exception):
            Message(id="1", author_id="u1", author_name="A", content="x")  # missing timestamp 
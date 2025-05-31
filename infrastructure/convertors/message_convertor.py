from domain.entities.message import Message
from infrastructure.persistence.message_document import MessageDocument

class MessageConvertor:
    """
    Factory for converting between domain Message and persistence MessageDocument.
    This ensures the domain model remains pure and decoupled from storage concerns.
    """
    @staticmethod
    def to_document(message: Message) -> MessageDocument:
        """
        Convert a domain Message to a persistence MessageDocument.
        All fields直接展开，id->message_id。
        """
        return MessageDocument(
            message_id=message.id,
            author_id=message.author_id,
            author_name=message.author_name,
            content=message.content,
            timestamp=message.timestamp
        )

    @staticmethod
    def to_entity(doc: MessageDocument) -> Message:
        """
        Convert a persistence MessageDocument to a domain Message.
        """
        return Message(
            id=doc.message_id,
            author_id=doc.author_id,
            author_name=doc.author_name,
            content=doc.content,
            timestamp=doc.timestamp
        ) 
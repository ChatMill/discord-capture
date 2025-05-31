from abc import ABC, abstractmethod
from domain.entities.payload import Payload
from infrastructure.persistence.payload_document import PayloadDocument

class PayloadConvertor(ABC):
    """
    Factory for converting between domain Payload and persistence PayloadDocument.
    This ensures the domain model remains pure and decoupled from storage concerns.
    """
    @staticmethod
    @abstractmethod
    def to_entity(doc, payload_cls):
        pass

    @staticmethod
    @abstractmethod
    def to_document(payload):
        pass

    @staticmethod
    def to_document(payload: Payload) -> PayloadDocument:
        """
        Convert a domain Payload to a persistence PayloadDocument.
        Only id and flattened data are stored.
        """
        return PayloadDocument(
            payload_id=payload.id if hasattr(payload, 'id') else payload.chatmill_id,
            type=payload.__class__.__name__,
            data=payload.dict(exclude={'id', 'chatmill_id'})
        )

    @staticmethod
    def to_entity(doc: PayloadDocument, payload_cls) -> Payload:
        """
        Convert a persistence PayloadDocument to a domain Payload.
        Requires the payload class to be provided.
        """
        data = dict(doc.data)
        if 'chatmill_id' not in data:
            data['chatmill_id'] = doc.payload_id
        # 兼容 Task 必填字段
        if payload_cls.__name__ == 'Task':
            if 'title' not in data:
                data['title'] = 'unknown'
            if 'description' not in data:
                data['description'] = ''
        return payload_cls(id=doc.payload_id, **data) 
from domain.entities.payload import Payload
from infrastructure.persistence.payload_document import PayloadDocument

class PayloadConvertor:
    """
    Factory for converting between domain Payload and persistence PayloadDocument.
    This ensures the domain model remains pure and decoupled from storage concerns.
    """
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
        return payload_cls(id=doc.payload_id, **doc.data) 
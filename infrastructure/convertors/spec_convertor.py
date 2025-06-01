from infrastructure.convertors.payload_convertor import PayloadConvertor
from domain.entities.spec import Spec
from infrastructure.persistence.payload_document import PayloadDocument

class SpecConvertor(PayloadConvertor):
    @staticmethod
    def to_entity(doc: PayloadDocument, payload_cls=Spec):
        data = dict(doc.data)
        if 'chatmill_id' not in data:
            data['chatmill_id'] = doc.payload_id
        if 'title' not in data:
            data['title'] = 'unknown'
        if 'description' not in data:
            data['description'] = ''
        return payload_cls(id=doc.payload_id, **data)

    @staticmethod
    def to_document(payload: Spec) -> PayloadDocument:
        return PayloadDocument(
            payload_id=payload.id if hasattr(payload, 'id') else payload.chatmill_id,
            type=payload.__class__.__name__,
            data=payload.dict(exclude={'id', 'chatmill_id'})
        ) 
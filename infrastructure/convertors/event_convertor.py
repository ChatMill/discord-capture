from domain.events.capture import Capture
from infrastructure.persistence.event_document import EventDocument
from typing import List
from domain.entities.spec import Spec
from domain.entities.payload import Payload
from infrastructure.convertors.payload_convertor import PayloadConvertor
from infrastructure.persistence.payload_document import PayloadDocument

class EventConvertor:
    """
    Factory for converting between domain Event (Capture) and persistence EventDocument.
    This ensures the domain model remains pure and decoupled from storage concerns.
    """
    @staticmethod
    def to_document(event: Capture) -> EventDocument:
        """
        Convert a domain Event (Capture) to a persistence EventDocument.
        Only id references are stored for related entities.
        不再存储 history 字段。
        """
        return EventDocument(
            event_id=event.event_id,
            session_id=event.session_id,
            operator_id=event.operator_id,
            payload_id=event.payload.id if hasattr(event.payload, 'id') else event.payload.chatmill_id,
            message_ids=[m.id for m in getattr(event, 'messages', [])],
            agent_profile=event.agent_profile.dict() if hasattr(event.agent_profile, 'dict') else dict(event.agent_profile),
            event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            agent=getattr(event, 'agent', '')
        )

    @staticmethod
    def to_entity(doc: EventDocument, payload, messages: List, agent_profile) -> Capture:
        """
        Convert a persistence EventDocument to a domain Event (Capture).
        Requires the referenced payload, messages, and agent_profile to be provided.
        history 字段由外部维护，不从 doc 读取。
        """
        # 统一用 PayloadConvertor.to_entity 还原 payload 为 Spec
        if not isinstance(payload, Spec):
            if isinstance(payload, PayloadDocument):
                payload = PayloadConvertor.to_entity(payload, Spec)
            elif isinstance(payload, Payload):
                # 先转 dict 再转 PayloadDocument
                payload_doc = PayloadDocument(payload_id=getattr(payload, 'id', None) or getattr(payload, 'chatmill_id', None), type=payload.__class__.__name__, data=payload.dict(exclude={'id', 'chatmill_id'}))
                payload = PayloadConvertor.to_entity(payload_doc, Spec)
            elif isinstance(payload, dict):
                payload_doc = PayloadDocument(**payload)
                payload = PayloadConvertor.to_entity(payload_doc, Spec)
            else:
                # 兜底，直接抛错
                raise ValueError("Unsupported payload type for event conversion")
        return Capture(
            event_id=doc.event_id,
            session_id=doc.session_id,
            operator_id=doc.operator_id,
            payload=payload,
            messages=messages,
            agent_profile=agent_profile,
            history=[],  # 由外部维护
            event_type=doc.event_type,
            agent=getattr(doc, 'agent', '')
        ) 
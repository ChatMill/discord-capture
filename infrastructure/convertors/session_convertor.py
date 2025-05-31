from domain.entities.session import Session
from infrastructure.persistence.session_document import SessionDocument

class SessionConvertor:
    """
    Factory for converting between domain Session and persistence SessionDocument.
    This ensures the domain model remains pure and decoupled from storage concerns.
    """
    @staticmethod
    def to_document(session: Session) -> SessionDocument:
        """
        Convert a domain Session to a persistence SessionDocument.
        Only id references are stored for related entities.
        """
        return SessionDocument(
            session_id=session.session_id,
            source=session.source.dict() if hasattr(session.source, 'dict') else dict(session.source),
            payload_id=session.payload.id if hasattr(session.payload, 'id') else session.payload.chatmill_id,
            history=session.history,
            agent=session.agent
        )

    @staticmethod
    def to_entity(doc: SessionDocument, source, payload) -> Session:
        """
        Convert a persistence SessionDocument to a domain Session.
        Requires the referenced source and payload to be provided.
        """
        return Session(
            session_id=doc.session_id,
            source=source,
            payload=payload,
            history=doc.history,
            agent=doc.agent
        ) 
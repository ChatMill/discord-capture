from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.session_repository import SessionRepository
from domain.entities.session import Session
from infrastructure.persistence.session_document import SessionDocument
from infrastructure.convertors.session_convertor import SessionConvertor
from infrastructure.persistence.payload_document import PayloadDocument
from infrastructure.convertors.payload_convertor import PayloadConvertor
from domain.entities.payload import Payload
from domain.value_objects.source import Source


class SessionRepositoryImpl(SessionRepository):
    """
    MongoDB's implementation of SessionRepository using motor.
    Uses SessionConvertor to convert between domain Session and persistence SessionDocument.
    Only stores id references for related entities (payload, etc.).
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["sessions"]
        self.payload_collection = db["payloads"]

    async def insert(self, session: Session) -> Any:
        """
        Upsert a session document by session_id into MongoDB.
        Converts domain Session to SessionDocument for storage.
        """
        doc = SessionConvertor.to_document(session)
        result = await self.collection.update_one(
            {"session_id": doc.session_id},
            {"$set": doc.dict()},
            upsert=True
        )
        return result.upserted_id or doc.session_id

    async def find(self, query: Dict[str, Any]) -> Optional[Session]:
        """
        Find a session document by query in MongoDB and convert to domain Session.
        Loads referenced payload and source as needed.
        """
        doc_dict = await self.collection.find_one(query)
        if not doc_dict:
            return None
        doc = SessionDocument(**doc_dict)
        # 加载 payload
        payload_doc_dict = await self.payload_collection.find_one({"payload_id": doc.payload_id})
        if not payload_doc_dict:
            return None
        payload_doc = PayloadDocument(**payload_doc_dict)
        payload = PayloadConvertor.to_entity(payload_doc, Payload)
        # 组装 source
        source = Source(**doc.source)
        return SessionConvertor.to_entity(doc, source, payload)

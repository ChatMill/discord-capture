from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.payload_repository import PayloadRepository
from infrastructure.persistence.payload_document import PayloadDocument
from infrastructure.convertors.payload_convertor import PayloadConvertor
from domain.entities.payload import Payload


class PayloadRepositoryImpl(PayloadRepository):
    """
    MongoDB's implementation of PayloadRepository using motor.
    Uses PayloadConvertor to convert between domain Payload and persistence PayloadDocument.
    Only stores minimal fields and id references.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["payloads"]

    async def insert(self, payload: Payload) -> Any:
        """
        Upsert a payload document by payload_id (chatmill_id) into MongoDB.
        Converts domain Payload to PayloadDocument for storage.
        """
        doc = PayloadConvertor.to_document(payload)
        result = await self.collection.update_one(
            {"payload_id": doc.payload_id},
            {"$set": doc.dict()},
            upsert=True
        )
        return result.upserted_id or doc.payload_id

    async def find(self, query: Dict[str, Any]) -> Optional[Payload]:
        """
        Find a payload document by query in MongoDB and convert to domain Payload.
        """
        doc_dict = await self.collection.find_one(query)
        if not doc_dict:
            return None
        doc = PayloadDocument(**doc_dict)
        return PayloadConvertor.to_entity(doc, Payload)

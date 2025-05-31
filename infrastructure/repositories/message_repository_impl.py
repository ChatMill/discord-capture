from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.message_repository import MessageRepository
from infrastructure.persistence.message_document import MessageDocument
from infrastructure.convertors.message_convertor import MessageConvertor
from domain.entities.message import Message


class MessageRepositoryImpl(MessageRepository):
    """
    MongoDB's implementation of MessageRepository using motor.
    Uses MessageConvertor to convert between domain Message and persistence MessageDocument.
    Only stores minimal fields and id references.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["messages"]

    async def insert(self, message: Message) -> Any:
        """
        Upsert a message document by message_id (id) into MongoDB.
        Converts domain Message to MessageDocument for storage.
        """
        doc = MessageConvertor.to_document(message)
        result = await self.collection.update_one(
            {"message_id": doc.message_id},
            {"$set": doc.dict()},
            upsert=True
        )
        return result.upserted_id or doc.message_id

    async def find(self, query: Dict[str, Any]) -> Optional[Message]:
        """
        Find a message document by query in MongoDB and convert to domain Message.
        """
        doc_dict = await self.collection.find_one(query)
        if not doc_dict:
            return None
        doc = MessageDocument(**doc_dict)
        return MessageConvertor.to_entity(doc)

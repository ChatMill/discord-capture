from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.message_repository import MessageRepository


class MessageRepositoryImpl(MessageRepository):
    """
    MongoDB's implementation of MessageRepository using motor.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["messages"]

    async def insert(self, message: Dict[str, Any]) -> Any:
        """Upsert a message document by id into MongoDB."""
        result = await self.collection.update_one(
            {"id": message["id"]},
            {"$set": message},
            upsert=True
        )
        return result.upserted_id or message["id"]

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a message document by query in MongoDB."""
        return await self.collection.find_one(query)

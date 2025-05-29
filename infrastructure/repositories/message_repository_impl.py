from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.message_repository import MessageRepository

class MessageRepositoryImpl(MessageRepository):
    """
    MongoDB implementation of MessageRepository using motor.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["messages"]

    async def insert(self, message: Dict[str, Any]) -> Any:
        """Insert a message document into MongoDB."""
        result = await self.collection.insert_one(message)
        return result.inserted_id

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a message document by query in MongoDB."""
        return await self.collection.find_one(query) 
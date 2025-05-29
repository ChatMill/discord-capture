from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.payload_repository import PayloadRepository

class PayloadRepositoryImpl(PayloadRepository):
    """
    MongoDB implementation of PayloadRepository using motor.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["payloads"]

    async def insert(self, payload: Dict[str, Any]) -> Any:
        """Insert a payload document into MongoDB."""
        result = await self.collection.insert_one(payload)
        return result.inserted_id

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a payload document by query in MongoDB."""
        return await self.collection.find_one(query) 
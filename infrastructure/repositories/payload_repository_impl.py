from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.payload_repository import PayloadRepository


class PayloadRepositoryImpl(PayloadRepository):
    """
    MongoDB's implementation of PayloadRepository using motor.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["payloads"]

    async def insert(self, payload: Dict[str, Any]) -> Any:
        """Upsert a payload document by chatmill_id into MongoDB."""
        result = await self.collection.update_one(
            {"chatmill_id": payload["chatmill_id"]},
            {"$set": payload},
            upsert=True
        )
        return result.upserted_id or payload["chatmill_id"]

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a payload document by query in MongoDB."""
        return await self.collection.find_one(query)

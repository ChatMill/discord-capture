from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.event_repository import EventRepository


class EventRepositoryImpl(EventRepository):
    """
    MongoDB implementation of EventRepository using motor.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["events"]

    async def insert(self, event: Dict[str, Any]) -> Any:
        """Upsert an event document by event_id into MongoDB."""
        result = await self.collection.update_one(
            {"event_id": event["event_id"]},
            {"$set": event},
            upsert=True
        )
        return result.upserted_id or event["event_id"]

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find an event document by query in MongoDB."""
        return await self.collection.find_one(query)

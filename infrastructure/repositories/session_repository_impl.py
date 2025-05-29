from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.session_repository import SessionRepository

class SessionRepositoryImpl(SessionRepository):
    """
    MongoDB implementation of SessionRepository using motor.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["sessions"]

    async def insert(self, session: Dict[str, Any]) -> Any:
        """Insert a session document into MongoDB."""
        result = await self.collection.insert_one(session)
        return result.inserted_id

    async def find(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a session document by query in MongoDB."""
        return await self.collection.find_one(query) 
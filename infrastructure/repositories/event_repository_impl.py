from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from domain.repositories.event_repository import EventRepository
from domain.events.capture import Capture
from infrastructure.persistence.event_document import EventDocument
from infrastructure.convertors.event_convertor import EventConvertor
from infrastructure.persistence.payload_document import PayloadDocument
from infrastructure.convertors.payload_convertor import PayloadConvertor
from infrastructure.convertors.spec_convertor import SpecConvertor
from infrastructure.persistence.message_document import MessageDocument
from infrastructure.convertors.message_convertor import MessageConvertor
from domain.entities.payload import Payload
from domain.value_objects.agent_profile import AgentProfile


class EventRepositoryImpl(EventRepository):
    """
    MongoDB's implementation of EventRepository using motor.
    Uses EventConvertor to convert between domain Event and persistence EventDocument.
    Only stores id references for related entities (payload, messages, etc.).
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["events"]
        self.payload_collection = db["payloads"]
        self.message_collection = db["messages"]

    async def insert(self, event: Capture) -> Any:
        """
        Upsert an event document by event_id into MongoDB.
        Converts domain Event to EventDocument for storage.
        """
        doc = EventConvertor.to_document(event)
        result = await self.collection.update_one(
            {"event_id": doc.event_id},
            {"$set": doc.dict()},
            upsert=True
        )
        return result.upserted_id or doc.event_id

    async def find(self, query: Dict[str, Any]) -> Optional[Capture]:
        """
        Find an event document by query in MongoDB and convert to domain Event.
        Loads referenced payload and messages as needed.
        """
        doc_dict = await self.collection.find_one(query)
        if not doc_dict:
            return None
        doc = EventDocument(**doc_dict)
        # 加载 payload，动态选择 convertor
        payload_doc_dict = await self.payload_collection.find_one({"payload_id": doc.payload_id})
        if not payload_doc_dict:
            return None
        payload_doc = PayloadDocument(**payload_doc_dict)
        # 动态选择 agent 类型
        agent = getattr(doc, 'agent', 'missspec')
        if agent == 'missspec':
            payload = SpecConvertor.to_entity(payload_doc)
        else:
            payload = PayloadConvertor.to_entity(payload_doc, Payload)
        # 加载 messages
        messages = []
        for mid in doc.message_ids:
            msg_doc_dict = await self.message_collection.find_one({"message_id": mid})
            if msg_doc_dict:
                msg_doc = MessageDocument(**msg_doc_dict)
                messages.append(MessageConvertor.to_entity(msg_doc))
        # 组装 agent_profile
        agent_profile = AgentProfile(**doc.agent_profile)
        return EventConvertor.to_entity(doc, payload, messages, agent_profile)

from typing import List
from domain.entities.message import Message


class MessageFetcherService:
    """
    Domain service for fetching and validating Discord messages.
    """
    def __init__(self, discord_client):
        self.discord_client = discord_client

    async def fetch_messages(self, channel_id: int, message_ids: List[int]) -> List[Message]:
        """
        Fetch multiple messages by their IDs from a given channel.
        """
        raw_messages = await self.discord_client.fetch_messages(channel_id, message_ids)
        messages = [
            Message(
                id=msg.id,
                content=msg.content,
                author_id=msg.author.id,
                author_name=getattr(msg.author, 'display_name', str(msg.author)),
                timestamp=msg.created_at
            )
            for msg in raw_messages if msg is not None
        ]
        return messages 
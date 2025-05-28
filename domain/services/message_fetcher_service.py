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
        Fetch multiple messages by their IDs from a given channel, and transform them into domain Message entities.
        Args:
            channel_id: The Discord channel ID
            message_ids: List of message IDs to fetch
        Returns:
            List of Message domain entities (skip None)
        """
        channel = self.discord_client.get_channel(channel_id) or await self.discord_client.fetch_channel(channel_id)
        messages = []
        for mid in message_ids:
            try:
                msg = await channel.fetch_message(mid)
                messages.append(
                    Message(
                        message_id=msg.id,
                        content=msg.content,
                        author_id=msg.author.id,
                        author_name=getattr(msg.author, 'display_name', str(msg.author)),
                        timestamp=msg.created_at
                    )
                )
            except Exception as e:
                print(f"[fetch_messages] Failed to fetch message {mid} in channel {channel_id}: {e}")
        return messages
